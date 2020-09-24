from flask import Blueprint, request, Response, jsonify
from classes import DatabaseConnection

search = Blueprint('search', __name__)

# @search.route("/<search_string>", methods=["GET"])
# def database_search(search_string):
#     search_term = search_string.tolower()
    
#     #TODO create SQL search query for searching multiple fields based on input

@search.route('/recent-titles', methods=["GET"])
def recent_titles():
    query = "SELECT * FROM books b LEFT JOIN authors a ON b.books_author_id = a.authors_id ORDER BY b.books_date_added DESC LIMIT 10"

    conn = DatabaseConnection()
    conn.db_connect()
    resp = conn.db_read(query = query, format_type = "book")
    conn.db_close()

    return jsonify({"books": resp})