import os
import mysql.connector
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306)),
}

SCHEMA_DIR = BASE_DIR / "app" / "schema"

def run_sql_file(cursor, file_path):
    print(f"Running: {file_path.name}")
    with open(file_path, "r", encoding="utf-8") as f:
        sql = f.read()

    statements = sql.split(";")
    for statement in statements:
        stmt = statement.strip()
        if stmt:
            cursor.execute(stmt)

def main():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        sql_files = sorted(SCHEMA_DIR.glob("*.sql"))

        for file in sql_files:
            run_sql_file(cursor, file)

        conn.commit()
        cursor.close()
        conn.close()

        print("All schema executed successfully.")

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
