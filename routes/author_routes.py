from flask import Blueprint, request, Response, jsonify
from utils import auth_utils as au
from classes import DatabaseConnection
from flask_cors import CORS

author = Blueprint('author', __name__)
CORS(author, supports_credentials=True)

@author.route('/create', methods=["POST"])
def create_author():
    decoded_token = au.validate_jwt_token(request.cookies.get('token'))

    if decoded_token['role'] == 'admin':
        last_name = request.json['last_name']
        first_name = request.json['first_name']

        query = "INSERT INTO authors(authors_last_name, authors_first_name) VALUES(%s, %s);"
        values = (last_name, first_name)

        conn = DatabaseConnection()
        conn.db_connect()
        resp = conn.db_write(query=query, vals=values)
        conn.db_close()

        return jsonify({"authors": resp})
    else:
        return Response(status=401)


@author.route("/update", methods=["PATCH"])
def update_author():
    decoded_token = au.validate_jwt_token(request.json["jwt_token"])

    if decoded_token['role'] == 'admin':
        data = request.json['form_input']

        author_id = data['author_id']
        last_name = data['last_name']
        first_name = data['first_name']

        query = "UPDATE authors SET authors_last_name=%s, authors_first_name=%s WHERE authors_id=%s;"
        values = (last_name, first_name, author_id)

        conn = DatabaseConnection()
        conn.db_connect()
        resp = conn.db_write(query = query, vals = values)
        conn.db_close()

        return resp
    else:
        return Response(status=401)


@author.route("/delete", methods=["DELETE"])
def delete_author():
    decoded_token = au.validate_jwt_token(request.cookies.get('token'))
    if decoded_token['role'] == 'admin':
        
        query = "DELETE FROM authors WHERE authors_id=%s"
        values = (request.json["author_id"],)

        conn = DatabaseConnection()
        conn.db_connect()
        resp = conn.db_write(query = query, vals = values)
        conn.db_close()

        return resp
    else:
        return Response(status=401)


@author.route('/getall', methods=["GET"])
def get_all_authors():
    query = "SELECT * FROM authors"

    conn = DatabaseConnection()
    conn.db_connect()
    resp = conn.db_read(query=query, format_type="author")
    conn.db_close()

    return jsonify({"authors": resp})


@author.route('/<id>', methods=['GET'])
def get_one_author(id):
    query = "SELECT * FROM authors WHERE authors_id = %s"
    values = (id,)
    conn = DatabaseConnection()
    conn.db_connect()
    resp = conn.db_read(query=query, vals=values, format_type="author")
    conn.db_close()

    return jsonify({"authors": resp})


@author.route("/<id>/bib", methods=["GET"])
def get_author_biblio(id):
    books_query = "SELECT * FROM authors a LEFT JOIN books b ON a.authors_id = b.books_author_id WHERE a.authors_id = %s"
    author_query = "SELECT * FROM authors WHERE authors_id = %s"
    values = (id,)

    conn = DatabaseConnection()
    conn.db_connect()
    author = conn.db_read(query=author_query, vals=values, format_type="author")
    books = conn.db_read(query=books_query, vals=values, format_type="book")
    conn.db_close()

    return jsonify({
        "authors": author,
        "books": books
    })