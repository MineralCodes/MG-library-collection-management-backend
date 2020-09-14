import os
from flask import Flask, request, jsonify
import mysql.connector
import datetime

from classes import DatabaseConnection
from auth_blueprint import authentication

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(authentication, url_prefix="/auth")

#*****************Book Rutes********************

@app.route("/getall/books", methods=["GET"])
def get_all_books():
    query = "SELECT * FROM books b LEFT JOIN authors a ON b.books_author_id = a.authors_id"
    
    conn = DatabaseConnection()
    conn.db_connect()
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

@app.route("/create/book", methods=['post'])
def create_book_record():
    data = request.json
    title = data['title']
    author = data['author']
    isbn = data['isbn']
    pub_year = data['publication_year']
    date = datetime.datetime.now()

    query = "INSERT INTO books(books_title, books_author_id, books_isbn, books_pub_year, books_date_added) VALUES (%s, %s, %s, %s, %s);"
    values = (title, author, isbn, pub_year, date)

    conn = DatabaseConnection()
    conn.db_connect()
    resp = conn.db_book_query(query = query, query_vals = values, commit=True, date_time=date)
    conn.db_close()

    return jsonify({"books": resp})


#******************Author Routes***********************
@app.route('/getall/authors', methods=["GET"])
def get_all_authors():
    query = "SELECT * FROM authors"

    conn = DatabaseConnection()
    conn.db_connect()
    resp = conn.db_author_query(query=query, commit=False)
    conn.db_close()

    return jsonify({"authors": resp})

@app.route('/author/<id>', methods=['GET'])
def get_one_author(id):
    query = "SELECT * FROM authors WHERE authors_id = %s"
    values = (id,)
    conn = DatabaseConnection()
    conn.db_connect()
    resp = conn.db_author_query(query=query, vals=values)
    conn.db_close()

    return jsonify({"authors": resp})

@app.route('/create/author', methods=["POST"])
def create_author():
    last_name = request.json['last_name']
    first_name = request.json['first_name']

    query = "INSERT INTO authors(authors_last_name, authors_first_name) VALUES(%s, %s);"
    values = (last_name, first_name)

    conn = DatabaseConnection()
    conn.db_connect()
    resp = conn.db_author_query(query=query, vals=values, commit=True)
    conn.db_close()

    return jsonify({"authors": resp})

@app.route("/author/<id>/bib", methods=["GET"])
def get_author_biblio(id):
    books_query = "SELECT * FROM authors a LEFT JOIN books b ON a.authors_id = b.books_author_id WHERE a.authors_id = %s"
    author_query = "SELECT * FROM authors WHERE authors_id = %s"
    values = (id,)

    conn = DatabaseConnection()
    conn.db_connect()
    author = conn.db_author_query(query=author_query, vals=values)
    books = conn.db_book_query(query=books_query, query_vals=values)
    conn.db_close()

    return jsonify({
        "authors": author,
        "books": books
    })

@app.route("/test-env", methods=['GET'])
def test_env():
    conn = DatabaseConnection()
    conn.db_connect()

    return {
        "url": os.getenv("DATABASE_URL"), 
        "user": os.getenv("DATABASE_USER"), 
        "password": os.getenv("DATABASE_PASSWORD"), 
        "schema": os.getenv("DATABASE_SCHEMA")}

if __name__ == '__main__':
    app.run(debug=True)