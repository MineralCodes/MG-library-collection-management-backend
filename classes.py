import os
import mysql.connector

class DatabaseConnection:
    def __init__(self, query, query_type = "select"):
        self.query = query
        self.query_type = query_type
        self.database = None
        self.cursor = None

    def connect(self):
        try:
            self.database = mysql.connector.connect(
                host=os.getenv("DATABASE_URL"),
                user=os.getenv("DATABASE_UDER"),
                password=os.getenv("DATABASE_PASSWORD"),
                database=os.getenv("DATABASE_SCHEMA")
            )
            self.cursor = self.database.cursor(dictionary=True)
            print("database connected", self.database)
        except mysql.connector.Error as err:
            print(err)
    
    def connection_query(self):
        if self.database.is_connected():
            self.cursor.execute(self.query)

            response = self.cursor.fetchall()
            data = []

            for item in response:
                itemObject = {
                    "id": item["books_id"],
                    "title": item["books_title"],
                    "author": f"{item['authors_last_name']}, {item['authors_first_name']}",
                    "publication_year": item["books_pub_year"],
                    "isbn": item["books_isbn"],
                    "date_added": item["books_date_added"]
                }
            
                data.append(itemObject)
            return data
        else:
            print("database not connected")

    def close_connection(self):
        if self.database.is_connected():
            self.cursor.close()
            self.database.close()
            print("database connection closed")
        else:
            print("database not connected")



# ******************test area******************
# newConnQuery = """SELECT * FROM books b
#                 LEFT JOIN authors a
#                 ON b.books_author_id = a.authors_id"""

# newConn = DatabaseConnection(newConnQuery)

# newConn.connect()

# newConn.connection_query()

# newConn.close_connection()