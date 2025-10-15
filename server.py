from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app=Flask(__name__)
CORS(app)

# -- DB Help --
def get_db():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
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
    conn.close()

# -- ROUTES --
@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json
    conn = get_db()
    conn.execute("INSERT INTO users (name, expenditures, food_expend, travel_expend) VALUES (?, ?, ?, ?)",
                 (data["name"], float(data["expenditures"]), float(data["food_expend"]), float(data["travel_expend"])))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"}), 201

@app.route("/add_card", methods=["POST"])
def add_card():
    data = request.json
    conn = get_db()
    conn.execute("INSERT INTO cards (name, issuer, annual_fee, purpose) VALUES (?, ?, ?, ?)",
                (data["card_name"], data["issuer"], float(data["annual_fee"]), data["purpose"]))
    conn.commit()
    conn.close()
    return jsonify({"status": "card added"}), 201

@app.route("/cards", methods=["GET"])
def get_cards():
    conn = get_db()
    rows = conn.execute("SELECT * from cards").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db()
    rows = conn.execute("SELECT * from users").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=6969)