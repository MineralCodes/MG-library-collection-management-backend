from flask import Blueprint, request, Response, jsonify, make_response
from utils import auth_utils as au
from classes import DatabaseConnection
import datetime
from flask_cors import CORS

book = Blueprint('book', __name__)
CORS(book, supports_credentials=True)

@book.route("/create", methods=['post'])
def create_book_record():
    decoded_token = au.validate_jwt_token(request.cookies.get('token'))
    print(request.json)
    if decoded_token['role'] == 'admin':
        data = request.json['form_input']

        title = data['title']
        author = data['author']
        isbn = data['isbn']
        pub_year = data['publication_year']
        date = datetime.datetime.now()

        query = "INSERT INTO books(books_title, books_author_id, books_isbn, books_pub_year, books_date_added) VALUES (%s, %s, %s, %s, %s);"
        values = (title, author, isbn, pub_year, date)

        conn = DatabaseConnection()
        conn.db_connect()
        result = conn.db_write(query = query, vals = values)

        if result['response'] == 200:
            query = "SELECT * FROM books b LEFT JOIN authors a ON b.books_author_id = a.authors_id WHERE b.books_title = %s AND b.books_author_id = %s AND b.books_date_added = %s"
            values = (title, author, date)
            book = conn.db_read(query=query, vals=values, format_type="book")
            conn.db_close()

            return make_response({"books": book}, 200)
        else:
            conn.db_close()

            return Response(status=result['response'])
    else:
        return Response(status=401)


@book.route("/update", methods=["PATCH"])
def update_book():
    decoded_token = au.validate_jwt_token(request.cookies.get('token'))
    if decoded_token['role'] == 'admin':
        data = request.json['form_input']

        book_id = data['book_id']
        title = data['title']
        author = data['author']
        isbn = data['isbn']
        pub_year = data['publication_year']
        description = data['description']

        query = "UPDATE books SET books_title=%s, books_author_id=%s, books_isbn=%s, books_pub_year=%s, books_description=%s WHERE books_id=%s;"
        values = (title, author, isbn, pub_year, book_id, description)

        conn = DatabaseConnection()
        conn.db_connect()
        result = conn.db_write(query = query, vals = values)

        if result['response'] == 200:
            query = "SELECT * FROM books b LEFT JOIN authors a ON b.books_author_id = a.authors_id WHERE b.books_id = %s"
            values = (book_id,)
            book = conn.db_read(query=query, vals=values, format_type="book")
            conn.db_close()

            return make_response({"books": book}, 200)
        else:
            conn.db_close()

            return Response(status=result['response'])
    else:
        return Response(status=401)

@book.route("/delete/<id>", methods=["DELETE"])
def delete_book(id):
    decoded_token = au.validate_jwt_token(request.cookies.get('token'))
    if decoded_token['role'] == 'admin':
        
        query = "DELETE FROM books WHERE books_id=%s"
        values = (id,)

        conn = DatabaseConnection()
        conn.db_connect()
        result = conn.db_write(query = query, vals = values)
        conn.db_close()

        return Response(status=result['response'])
    else:
        return Response(status=401)

@book.route("/getall", methods=["GET"])
def get_all_books():
    query = "SELECT * FROM books b LEFT JOIN authors a ON b.books_author_id = a.authors_id"
    
    conn = DatabaseConnection()
    conn.db_connect()
    result = conn.db_read(format_type="book", query=query)
    conn.db_close()

    return make_response({"books": result}, 200)


@book.route("/<id>", methods=["GET"])
def get_one_book(id):
    query = "SELECT * FROM books b LEFT JOIN authors a ON b.books_author_id = a.authors_id WHERE b.books_id = %s"
    values = (id,)
    conn = DatabaseConnection()
    conn.db_connect()
    result = conn.db_read(format_type="book", query=query, vals=values)
    conn.db_close()

    return make_response({"books": result}, 200)

