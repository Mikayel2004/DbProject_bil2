# main.py

import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from pydbgen import pydbgen
from random import randint
from flask import Flask, jsonify, request
from datetime import date, timedelta, datetime

from DBInit import initDb
from DataGen import dbGen
from config import config

# Initialize the Flask app
app = Flask(__name__)

# Database connection function
def get_db_connection():
    db_params = config()
    return psycopg2.connect(
        host=db_params["host"],
        port=db_params["port"],
        user=db_params["db_owner"],
        password=db_params["admin_password"],
        dbname=db_params["db_name"],
        cursor_factory=RealDictCursor
    )

# Function to initialize the database
def initialize_database():
    print("Reading database configuration...")
    db_params = config()
    initDb(
        psycopg2=psycopg2,
        sql=sql,
        host=db_params["host"],
        port=db_params["port"],
        admin_user=db_params["admin_user"],
        admin_password=db_params["admin_password"],
        db_name=db_params["db_name"],
        db_owner=db_params["db_owner"],
    )
    print("Database initialization complete!")

# Flask Routes (API)
@app.route('/professors', methods=['GET'])
def get_professors():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM professor;")
                professors = cursor.fetchall()
        return jsonify(professors), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/professors/<int:id>', methods=['GET'])
def get_professor(id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM professor WHERE id = %s;", (id,))
                professor = cursor.fetchone()
        if professor:
            return jsonify(professor), 200
        else:
            return jsonify({"error": "Professor not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/professors', methods=['POST'])
def add_professor():
    data = request.json
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO professor (name, degree, department, position) VALUES (%s, %s, %s, %s) RETURNING *;",
                    (data['name'], data['degree'], data['department'], data['position'])
                )
                conn.commit()
                new_professor = cursor.fetchone()
        return jsonify(new_professor), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/professors/<int:id>', methods=['PUT'])
def update_professor(id):
    data = request.json
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE professor SET name = %s, degree = %s, department = %s, position = %s WHERE id = %s RETURNING *;",
                    (data['name'], data['degree'], data['department'], data['position'], id)
                )
                conn.commit()
                updated_professor = cursor.fetchone()
        if updated_professor:
            return jsonify(updated_professor), 200
        else:
            return jsonify({"error": "Professor not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/professors/<int:id>', methods=['DELETE'])
def delete_professor(id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM professor WHERE id = %s RETURNING *;", (id,))
                conn.commit()
                deleted_professor = cursor.fetchone()
        if deleted_professor:
            return jsonify(deleted_professor), 200
        else:
            return jsonify({"error": "Professor not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the API!"}), 200

# Expose app and initialize_database
if __name__ == '__main__':
    print("This file is not meant to be run directly. Use app.py instead.")
