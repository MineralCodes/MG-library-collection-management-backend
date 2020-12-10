from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# TESTING = False
# DEBUG = False
# FLASK_ENV = 'development'
CORS_HEADERS = 'Content-Type'
DATABASE_URL = environ.get("DATABASE_URL")
DATABASE_USER = environ.get("DATABASE_USER")
DATABASE_PASSWORD = environ.get("DATABASE_PASSWORD")
DATABASE_SCHEMA = environ.get("DATABASE_SCHEMA")