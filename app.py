import os
from flask import Flask, Request, jsonify
import mysql.connector
from classes import DatabaseConnection

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route("/getall", methods=["GET"])
def get_all_books():
    query = "SELECT * FROM books b LEFT JOIN authors a ON b.books_author_id = a.authors_id"
    
    conn = DatabaseConnection(query)
    conn.connect()
    resp = conn.connection_query()
    conn.close_connection()

    return jsonify({"books": resp})

@app.route("/book/<id>", methods=["GET"])
def get_one_book(id):
    query = f"SELECT * FROM books b LEFT JOIN authors a ON b.books_author_id = a.authors_id WHERE b.books_id = {id}"

    conn = DatabaseConnection(query)
    conn.connect()
    resp = conn.connection_query()
    conn.close_connection()

    return jsonify({"books": resp})

@app.route("/test-env")
def test_env():
    conn = DatabaseConnection("SELECT * FROM books")
    conn.connect()
    return {
        "url": os.getenv("DATABASE_URL"), 
        "user": os.getenv("DATABASE_USER"), 
        "password": os.getenv("DATABASE_PASSWORD"), 
        "schema": os.getenv("DATABASE_SCHEMA")}

if __name__ == '__main__':
    app.run(debug=True)