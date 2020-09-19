from flask import Flask, request, jsonify, Response
import datetime

from classes import DatabaseConnection
# from utils import validate_jwt_token

from routes import author_routes, book_routes, authentication_routes


app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(authentication_routes.authentication, url_prefix="/auth")
app.register_blueprint(book_routes.book, url_prefix="/book")
app.register_blueprint(author_routes.author, url_prefix="/author")


@app.route("/test-route", methods=['POST'])
def test():
    # token = request.json["jwt_token"]
    # decoded = validate_jwt_token(token)

    return "decoded"

if __name__ == '__main__':
    app.run(debug=True)