from flask import Blueprint, request, Response, jsonify, make_response
from utils import auth_utils as au
from classes import DatabaseConnection
from flask_cors import CORS

authentication = Blueprint('authentication', __name__)

CORS(authentication, supports_credentials=True)

@authentication.route("/register", methods=["POST"])
def register_user():
    user_email = request.json["email"]
    user_password = request.json["password"]
    user_confirm_password = request.json["confirm_password"]

    if user_password == user_confirm_password and au.validate_user_input(
        'authentication', email=user_email, password=user_password
    ):
        password_salt = au.generate_salt()
        password_hash = au.generate_hash(user_password, password_salt)

        query = "INSERT INTO users (users_email, users_password, users_password_salt, users_role) VALUES (%s, %s, %s, 'admin')"
        values = (user_email, password_hash, password_salt)

        conn = DatabaseConnection()

        conn.db_connect()
        
        if conn.db_write(query=query, vals=values):
            return Response(status=200)
        else:
            return Response(status=409)
    else:
        return Response(status=400)


@authentication.route("/login", methods=["POST"])
def login_user():
    user_email = request.json['email']
    user_password = request.json['password']

    query = "SELECT * FROM users WHERE users_email = %s"
    values = (user_email,)

    conn = DatabaseConnection()
    conn.db_connect()

    current_user = conn.db_read(query=query, vals=values, format_type="user")
    
    user_token = au.validate_user(current_user=current_user[0], password=user_password)
    resp = make_response()
    resp.headers["Content-Type"] = "application/json"
    resp.set_cookie('token', user_token, secure=True)

    if user_token:
        return resp 
    else:
        Response(status=401)


@authentication.route("/validate", methods=["post"])
def validate_user_role():
    token = request.cookies.get('token')
    decoded = au.validate_jwt_token(token)

    return jsonify({"_id": decoded['id'], "email": decoded['email'], "user_role": decoded['role']})