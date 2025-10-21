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
            credit_score REAL,
            credit_age REAL,
            monthly_dining REAL,
            monthly_groceries REAL,
            monthly_gas REAL,
            monthly_streaming REAL,
            monthly_online_shopping REAL,
            monthly_drugstore_pharmacy REAL,
                
            monthly_flights REAL,
            monthly_flights_portal REAL,
            monthly_hotel REAL,
            monthly_hotel_portal REAL,
            monthly_car_rental REAL,
            monthly_car_rental_portal REAL,
            monthly_travel REAL,
            monthly_other REAL
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
    cur.execute("INSERT INTO users (name, credit_score, credit_age, monthly_dining," + 
                "monthly_groceries, monthly_gas, monthly_streaming, monthly_online_shopping," + 
                "monthly_drugstore_pharmacy, monthly_flights, monthly_flights_portal," + 
                "monthly_hotel, monthly_hotel_portal, monthly_car_portal, monthly_car_rental_portal," +
                "monthly_travel, monthly_other) VALUES (%s, %s, %s, %s, %s, %s, %s, %s," +
                "%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                 (data["name"], data["credit_score"], data["credit_age"], data["monthly_dining"],
                  data["monthly_groceries"], data["monthly_gas"], data["monthly_streaming"],
                  data["monthly_online_shopping"], data["monthly_drugstore_pharmacy"], data["monthly_flights"],
                  data["monthly_flights_portal"], data["monthly_hotel"], data["monthly_hotel_portal"],
                  data["monthly_car_rental"], data["monthly_car_rental_portal"], data["monthly_travel"],
                  data["monthly_other"]))
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
                "credit_score": row[2],
                "credit_age": row[3],
                "monthly_dining": row[4],
                "monthly_groceries": row[5],
                "monthly_gas": row[6],
                "monthly_streaming": row[7],
                "monthly_online_shopping": row[8],
                "monthly_drugstore_pharmacy": row[9],
                "monthly_flights": row[10],
                "monthly_flights_portal": row[11],
                "monthly_hotel": row[12],
                "monthly_hotel_portal": row[13],
                "monthly_car_rental": row[14],
                "monthly_car_rental_portal": row[15],
                "monthly_travel": row[16],
                "monthly_other": row[17]
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