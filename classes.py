import os
import mysql.connector
from flask import Response

class DatabaseConnection:
    def __init__(self):
        # self.query = query
        # self.query_type = query_type
        # self.vals = vals
        self.database = None
        self.cursor = None


    def generate_response_object(self, rows, format_type):
        data = []

        if format_type == "author":
            for row in rows:
                res_object = {
                        "id": row['authors_id'],
                        "last_name": row['authors_last_name'],
                        "first_name": row['authors_first_name'],
                        "full_name": f"{row['authors_last_name']}, {row['authors_first_name']}"
                    }
                data.append(res_object)
        elif format_type == "book":
            for row in rows:
                res_object = {
                            "id": row["books_id"],
                            "title": row["books_title"],
                            "author": f"{row['authors_last_name']}, {row['authors_first_name']}",
                            "publication_year": row["books_pub_year"],
                            "description": row['books_description'],
                            "isbn": row["books_isbn"],
                            "date_added": row["books_date_added"]
                        }
                data.append(res_object)
        elif format_type == "user":
            for row in rows:
                data.append(row)
        
        return data


    def db_connect(self):
        try:
            self.database = mysql.connector.connect(
                host=os.getenv("DATABASE_URL"),
                user=os.getenv("DATABASE_USER"),
                password=os.getenv("DATABASE_PASSWORD"),
                database=os.getenv("DATABASE_SCHEMA")
            )
            self.cursor = self.database.cursor(dictionary=True)
        except mysql.connector.Error as err:
            return "error in db_connect fucntion", err
    

    def db_read(self, format_type, query, vals=None):
        if self.database.is_connected():
            try:
                self.cursor.execute(query, vals)
                response = self.cursor.fetchall()

                results = self.generate_response_object(response, format_type)

                return results

            except mysql.connector.Error as err:
                return f"error in db_read fucntion: {err}"

    def db_write(self, query, vals=None):
        if self.database.is_connected():
            try:
                self.cursor.execute(query, vals)
                self.database.commit()
                return { "result": True, "response": 200}
            except mysql.connector.Error as err:
                print(f"error in db_write function: {err}")
                return {"result": False, "response": 401}
        else:
            return Response(status=500)

    def db_close(self):
        if self.database.is_connected():
            self.cursor.close()
            self.database.close()
        else:
            print("database not connected")