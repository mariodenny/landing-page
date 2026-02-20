from flask import Blueprint, render_template
import mysql.connector
import os
from dotenv import load_dotenv
from pathlib import Path

main = Blueprint("main", __name__)

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

@main.route("/")
def home():
    return render_template("index.html")


@main.route("/leaderboard")
def leaderboard():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT name, total_spent
        FROM customer_stats
        ORDER BY total_spent DESC
        LIMIT 10
    """)

    customers = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("leaderboard.html", customers=customers)


@main.route("/about")
def about():
    return render_template("about.html")
