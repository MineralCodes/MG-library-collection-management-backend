from flask import Flask, Request, jsonify
import mysql.connector

app = Flask(__name__)

database = mysql.connector.connect(
    host="us-cdbr-east-02.cleardb.com",
    user="bd5a2a7ea12005",
    password="af98e11b",
    database="heroku_b1552496830e89b"
)

cursor = database.cursor(dictionary=True)

# for x in cursor:
#   print(x["books_title"]) 

@app.route("/all-books")
def get_all_books():
    cursor.execute("SELECT * FROM books")
    data = {}
    for idx,item in enumerate(cursor):
        data.update({idx: item})

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)