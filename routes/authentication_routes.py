import datetime
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
        
        created = conn.db_write(query=query, vals=values)
        if created['result']:
            user_query = "SELECT * FROM users WHERE users_email = %s"
            current_user = conn.db_read(query=user_query, vals=(user_email,), format_type="user")
    
            if len(current_user) > 0:
                user_info = current_user[0]
                user_token = au.validate_user(current_user=user_info, password=user_password)

                if user_token:
                    expire_date = datetime.datetime.now()
                    expire_date = expire_date + datetime.timedelta(days=365)
                    resp = make_response({"user": {"email": user_info['users_email'], "id": user_info['users_id'], "user_role": user_info['users_role']}}, 200)
                    resp.headers["content-type"] = "application/json"
                    resp.set_cookie('token', user_token, secure=True, httponly=False, expires=expire_date, domain='.heroku.com')
                    return resp 
                else:
                    return Response(status=401)
            else:
                return Response(status=400)
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
    
    if len(current_user) > 0:
        user_info = current_user[0]
        user_token = au.validate_user(current_user=user_info, password=user_password)

        if user_token:
            expire_date = datetime.datetime.now()
            expire_date = expire_date + datetime.timedelta(days=365)
            resp = make_response({"user": {"email": user_info['users_email'], "id": user_info['users_id'], "user_role": user_info['users_role']}}, 200)
            resp.headers["content-type"] = "application/json"
            resp.set_cookie('token', user_token, secure=True, httponly=False, expires=expire_date, domain='.heroku.com')
            return resp 
        else:
            return Response(status=401)
    else:
        return Response(status=404)

@authentication.route("/logout", methods=["POST"])
def logout_user():
    expire_date = datetime.datetime.now()
    expire_date = expire_date + datetime.timedelta(days=-1)
    resp = make_response()
    resp.delete_cookie('token')

    return resp


@authentication.route("/validate", methods=["POST"])
def validate_user_role():
    token = request.cookies.get('token')
    decoded = au.validate_jwt_token(token)

    return jsonify({"id": decoded['id'], "email": decoded['email'], "user_role": decoded['role']})


@authentication.route("/update-password", methods=["POST"])
def update_user_password():
    user_id = request.json['id']
    old_password = request.json['password']
    new_password = request.json['new_password']
    confirm_password = request.json['confirm_password']

    query = "SELECT * FROM users WHERE users_id = %s"
    
    conn = DatabaseConnection()
    conn.db_connect()


    current_user = conn.db_read(query=query, vals=(user_id,), format_type="user")

    if len(current_user) > 0:
        user_info = current_user[0]

        user_password = user_info['users_password']
        user_password_salt = user_info['users_password_salt']

        old_password_hash = au.generate_hash(old_password, user_password_salt)

        if old_password_hash == user_password:
            if new_password == confirm_password:
                new_password_hash = au.generate_hash(new_password, user_password_salt)

                update_query = "UPDATE users SET users_password = %s WHERE users_id = %s"
                values = (new_password_hash, user_id)

                conn.db_write(query=update_query, vals=values)

                conn.db_close()
                return Response(status=200)
            else:
                conn.db_close()
                return Response(status=406)
        else:
            conn.db_close()
            return Response(status=401)
    else:
        conn.db_close()
        return Response(status=404)