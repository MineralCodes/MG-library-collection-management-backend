import os
from flask import Flask, request, jsonify
import mysql.connector
import datetime

from classes import DatabaseConnection

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route("/getall", methods=["GET"])
def get_all_books():
    query = "SELECT * FROM books b LEFT JOIN authors a ON b.books_author_id = a.authors_id"
    
    conn = DatabaseConnection()
    conn.connect()
    resp = conn.db_book_query(query)
    conn.db_close()

    return jsonify({"books": resp})

@app.route("/book/<id>", methods=["GET"])
def get_one_book(id):
    query = "SELECT * FROM books b LEFT JOIN authors a ON b.books_author_id = a.authors_id WHERE b.books_id = %s"
    vals = id
    conn = DatabaseConnection()
    conn.db_connect()
    resp = conn.db_book_query(query, vals)
    conn.db_close()

    return jsonify({"books": resp})

@app.route("/create", methods=['post'])
def create_record():
    data = request.json
    title = data['title']
    author = data['author']
    isbn = data['isbn']
    pub_year = data['publication_year']
    date = datetime.datetime.now()

    query = "INSERT INTO books(books_title, books_author_id, books_isbn, books_pub_year, books_date_added) VALUES (%s, %s, %s, %s, %s);"
    values = (title, author, isbn, pub_year, date)

    conn = DatabaseConnection()
    conn.connect()
    resp = conn.db_book_query(query = query, query_vals = values, commit=True, date_time=date)
    conn.db_close()

    return jsonify({"books": resp})


@app.route("/test-env")
def test_env():
    conn = DatabaseConnection()
    conn.connect()
    return {
        "url": os.getenv("DATABASE_URL"), 
        "user": os.getenv("DATABASE_USER"), 
        "password": os.getenv("DATABASE_PASSWORD"), 
        "schema": os.getenv("DATABASE_SCHEMA")}

if __name__ == '__main__':
    app.run(debug=True)