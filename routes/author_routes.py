from flask import Blueprint, request, Response, jsonify
from utils import auth_utils as au
from classes import DatabaseConnection

author = Blueprint('author', __name__)

@author.route('/create', methods=["POST"])
def create_author():
    decoded_token = au.validate_jwt_token(request.json["jwt_token"])

    if decoded_token['role'] == 'admin':
        last_name = request.json['last_name']
        first_name = request.json['first_name']

        query = "INSERT INTO authors(authors_last_name, authors_first_name) VALUES(%s, %s);"
        values = (last_name, first_name)

        conn = DatabaseConnection()
        conn.db_connect()
        resp = conn.db_author_query(query=query, vals=values, commit=True)
        conn.db_close()

        return jsonify({"authors": resp})
    else:
        return Response(status=401)


@author.route('/getall', methods=["GET"])
def get_all_authors():
    query = "SELECT * FROM authors"

    conn = DatabaseConnection()
    conn.db_connect()
    resp = conn.db_author_query(query=query)
    conn.db_close()

    return jsonify({"authors": resp})


@author.route('/<id>', methods=['GET'])
def get_one_author(id):
    query = "SELECT * FROM authors WHERE authors_id = %s"
    values = (id,)
    conn = DatabaseConnection()
    conn.db_connect()
    resp = conn.db_author_query(query=query, vals=values)
    conn.db_close()

    return jsonify({"authors": resp})


@author.route("/<id>/bib", methods=["GET"])
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