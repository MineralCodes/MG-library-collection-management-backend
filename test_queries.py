import mysql.connector

database = mysql.connector.connect(
    host="us-cdbr-east-02.cleardb.com",
    user="bd5a2a7ea12005",
    password="af98e11b",
    database="heroku_b1552496830e89b"
)

cursor = database.cursor(dictionary=True)

cursor.execute(f"SELECT * FROM authors WHERE authors_id = {1}")
author = cursor.fetchone()

print(author)

os.getenv("DATABASE_URL"), os.getenv("DATABASE_USER"), os.getenv("DATABASE_PASSWORD"), os.getenv("DATABASE_SCHEMA")