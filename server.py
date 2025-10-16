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
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT,
            expenditures REAL,
            food_expend REAL,
            travel_expend REAL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cards (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            issuer TEXT,
            annual_fee REAL,
            purpose TEXT
        )     
    """)
    conn.commit()
    cur.close()
    conn.close()
init_db()

# -- ROUTES --
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, expenditures, food_expend, travel_expend) VALUES (%s, %s, %s, %s)",
                 (data["name"], data["expenditures"], data["food_expend"], data["travel_expend"]))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "success"}), 201

@app.route("/add_card", methods=["POST"])
def add_card():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO cards (name, issuer, annual_fee, purpose) VALUES (%s, %s, %s, %s)",
                (data["card_name"], data["issuer"], data["annual_fee"], data["purpose"]))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "card added"}), 201

@app.route("/cards", methods=["GET"])
def get_cards():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * from cards")
        rows = cur.fetchall()
        
        cards = []
        for row in rows:
            cards.append({
                "id": row[0],
                "name": row[1],
                "issuer": row[2],
                "annual_fee": row[3],
                "purpose": row[4]
            })

        cur.close()
        conn.close()
        return jsonify(cards), 200
    except Exception as e:
        print("Error fetching cards:", e)
        return jsonify({'error': str(e)}), 500


@app.route("/users", methods=["GET"])
def get_users():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * from users")
        rows = cur.fetchall()
        
        users = []
        for row in rows:
            users.append({
                "id": row[0],
                "name": row[1],
                "user_expend": row[2],
                "food_expend": row[3],
                "travel_expend": row[4]
            })

        cur.close()
        conn.close()
        return jsonify(users), 200
    except Exception as e:
        print("Error fetching users:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 6969))
    app.run(host="0.0.0.0", port=port)