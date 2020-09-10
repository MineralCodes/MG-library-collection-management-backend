# import mysql.connector
import datetime

# database = mysql.connector.connect(
#     host="us-cdbr-east-02.cleardb.com",
#     user="bd5a2a7ea12005",
#     password="af98e11b",
#     database="heroku_b1552496830e89b"
# )

# cursor = database.cursor(dictionary=True)

# cursor.execute(f"INSERT INTO books(books_title, books_author_id, books_date_added) VALUES ('The Titans Curse', 1, CURRENT_DATE());")
# # author = cursor.fetchone()

# database.commit()

current_date = datetime.datetime.now()
print(current_date)