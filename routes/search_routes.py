from flask import Blueprint, request, Response, jsonify, make_response
from classes import DatabaseConnection
from flask_cors import CORS

search = Blueprint('search', __name__)

CORS(search, supports_credentials=True)

@search.route('/recent-titles', methods=["GET"])
def recent_titles():
    query = "SELECT * FROM books b LEFT JOIN authors a ON b.books_author_id = a.authors_id ORDER BY b.books_date_added DESC LIMIT 10"

    conn = DatabaseConnection()
    conn.db_connect()
    resp = conn.db_read(query=query, format_type="book")
    conn.db_close()

    return jsonify({"books": resp})

@search.route("/query", methods={"POST"})
def search_db():
    search_string = request.json["search_string"].lower().split("+")
    terms = ""
    
    idx = 0
    while idx < len(search_string):
        if idx < (len(search_string) - 1):
            terms += f"('%{search_string[idx]}%'),"
            idx += 1
        elif idx == (len(search_string) - 1):
            terms += f"('%{search_string[idx]}%')"
            idx += 1

    create_terms_temp_table_query = "CREATE TEMPORARY TABLE search (term VARCHAR(100));"
    drop_terms_temp_table_query = "DROP TEMPORARY TABLE search;"

    insert_terms_query = f"INSERT INTO search VALUES {terms};"

    select_books_query = """
        SELECT COUNT(b.books_id) AS hits, b.*, a.* FROM books b 
        LEFT JOIN authors a ON b.books_author_id = a.authors_id
        JOIN search s ON (LOWER(b.books_title) LIKE LOWER(s.term) OR LOWER(a.authors_first_name) LIKE LOWER(s.term) OR LOWER(a.authors_last_name) LIKE LOWER(s.term))
        GROUP BY b.books_id
        ORDER BY hits DESC;
        """
    
    conn = DatabaseConnection()
    conn.db_connect()
    
    create_table = conn.db_write(query=create_terms_temp_table_query)
    if create_table['result']:
        insert_terms = conn.db_write(query=insert_terms_query)
        if insert_terms['result']:
            resp = conn.db_read(query=select_books_query, format_type="book")
            conn.db_write(query=drop_terms_temp_table_query)
            return make_response({"books": resp}, 200)  ##jsonify({"books": resp })
        else:
            return make_response("query terms insert failed", 500)
    else:
        return make_response("failed to create terms table", 500)