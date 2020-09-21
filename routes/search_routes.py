from flask import Blueprint, request, Response, jsonify
from classes import DatabaseConnection

search = Blueprint('search', __name__)

@search.route("/<search_string>", methods=["GET"])
def search(search_string):
    search_term = search_string.tolower()
    
    #TODO create SQL search query for searching multiple fields based on input