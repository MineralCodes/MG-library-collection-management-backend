from flask import Blueprint, request, Response, jsonify
from utils import validate_user_input, generate_salt, generate_hash, validate_user
from classes import DatabaseConnection

authentication = Blueprint('authentication', __name__)

@authentication.route("/register", methods=["POST"])
def register_user():
    user_email = request.json["email"]
    user_password = request.json["password"]
    user_confirm_password = request.json["confirm_password"]

    if user_password == user_confirm_password and validate_user_input(
        'authentication', email=user_email, password=user_password
    ):
        password_salt = generate_salt()
        password_hash = generate_hash(user_password, password_salt)

        query = "INSERT INTO users (users_email, users_password, users_password_salt, users_role) VALUES (%s, %s, %s, 'Admin')"
        values = (user_email, password_hash, password_salt)

        conn = DatabaseConnection()

        conn.db_connect()
        if conn.db_create_user(query=query, vals=values, commit=True):
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
    
    current_user = conn.db_user_auth(query=query, vals=values)
    
    user_token = validate_user(current_user=current_user, password=user_password)

    if user_token:
        return jsonify({"jwt_token": user_token})
    else:
        Response(status=401)