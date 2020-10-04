from flask import Flask, request, jsonify, Response
import datetime
from flask_cors import CORS

from classes import DatabaseConnection
# from utils import validate_jwt_token

from routes import author_routes, book_routes, authentication_routes, search_routes


app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

app.config.from_pyfile('config.py')

app.register_blueprint(authentication_routes.authentication, url_prefix="/auth")
app.register_blueprint(book_routes.book, url_prefix="/book")
app.register_blueprint(author_routes.author, url_prefix="/author")
app.register_blueprint(search_routes.search, url_prefix="/search")

@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


@app.route("/test-route", methods=['POST'])
def test():
    # token = request.json["jwt_token"]
    # decoded = validate_jwt_token(token)

    return "decoded"

if __name__ == '__main__':
    app.run(threaded=True)