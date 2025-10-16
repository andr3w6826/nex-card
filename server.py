from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os
import psycopg2

app=Flask(__name__, static_folder='static')
CORS(app)
DATABASE_URL = os.getenv('DATABASE_URL')

# -- DB Help --
def get_db():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

def init_db():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            expenditures REAL,
            food_expend REAL,
            travel_expend REAL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            issuer TEXT,
            annual_fee REAL,
            purpose TEXT
        )     
    """)
    conn.commit()
    cur.close()
    conn.close()

# -- ROUTES --
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json
    conn = get_db()
    cur = conn.cursor
    cur.execute("INSERT INTO users (name, expenditures, food_expend, travel_expend) VALUES (?, ?, ?, ?)",
                 (data["name"], float(data["expenditures"]), float(data["food_expend"]), float(data["travel_expend"])))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "success"}), 201

@app.route("/add_card", methods=["POST"])
def add_card():
    data = request.json
    conn = get_db()
    cur = conn.cursor
    cur.execute("INSERT INTO cards (name, issuer, annual_fee, purpose) VALUES (?, ?, ?, ?)",
                (data["card_name"], data["issuer"], float(data["annual_fee"]), data["purpose"]))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "card added"}), 201

@app.route("/cards", methods=["GET"])
def get_cards():
    conn = get_db()
    cur = conn.cursor
    rows = cur.execute("SELECT * from cards").fetchall()
    cur.close()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db()
    cur = conn.cursor
    rows = cur.execute("SELECT * from users").fetchall()
    cur.close()
    conn.close()
    return jsonify([dict(r) for r in rows])

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 6969))
    app.run(host="0.0.0.0", port=port)