import os
from hashlib import pbkdf2_hmac
import jwt

def validate_user_input(input_type, **kwargs):
    if input_type == 'authentication':
        if len(kwargs["email"]) <= 255 and len(kwargs["password"]) <= 255:
            return True
        else:
            return False

def generate_salt():
    salt = os.urandom(16)
    return str(salt)


def generate_hash(text_password, password_salt):
    password_hash = pbkdf2_hmac(
        "sha256",
        b"%b" % bytes(text_password, "utf-8"),
        b"%b" % bytes(password_salt, "utf-8"),
        10000
    )

    return password_hash.hex()

def validate_user(current_user, password):
    if current_user:
        saved_password_hash = current_user['users_password']
        password_salt = current_user["users_password_salt"]
        password_hash = generate_hash(password, password_salt)

        if password_hash == saved_password_hash:
            user_id = current_user['users_id']
            user_role = current_user['users_role']
            jwt_token = generate_jwt_token({"id": user_id, "role": user_role})
            return jwt_token
        else:
            return False
    else:
        return False

def generate_jwt_token(content):
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    encoded_content = jwt.encode(content, JWT_SECRET_KEY, algorithm="HS256")
    token = str(encoded_content).split("'")[1]
    return token

def validate_jwt_token(token):
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    decoded_content = jwt.decode(token, JWT_SECRET_KEY, algorithm="HS256")

    return decoded_content