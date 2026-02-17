import os
from dotenv import load_dotenv
from mysql.connector import pooling
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306)),
}

connection_pool = pooling.MySQLConnectionPool(
    pool_name="zhubeauty_pool",
    pool_size=5,
    **DB_CONFIG
)

def get_db_connection():
    return connection_pool.get_connection()
