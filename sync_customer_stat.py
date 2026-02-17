import os
import requests
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path

# Load .env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

API_URL = os.getenv("ULTIPOS_API_URL")
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306)),
}

def fetch_from_api():
    print("Fetching data from Ultipos API...")
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    result = response.json()

    if not result.get("success"):
        raise Exception("API returned unsuccessful response")

    return result["data"]

def sync_to_db(data):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    for item in data:
        cursor.execute("""
            INSERT INTO customer_stats 
            (contact_id, name, total_transactions, total_spent, last_transaction_date, synced_at, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
            ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                total_transactions = VALUES(total_transactions),
                total_spent = VALUES(total_spent),
                last_transaction_date = VALUES(last_transaction_date),
                synced_at = VALUES(synced_at),
                updated_at = NOW()
        """, (
            item["contact_id"],
            item["name"],
            item["total_transactions"],
            item["total_spent"],
            item.get("last_transaction_date"),
            datetime.now()
        ))

    conn.commit()
    cursor.close()
    conn.close()

def main():
    try:
        data = fetch_from_api()
        sync_to_db(data)
        print("✅ Sync completed successfully.")
    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    main()
