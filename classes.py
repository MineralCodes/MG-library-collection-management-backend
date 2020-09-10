import os
import mysql.connector

class DatabaseConnection:
    def __init__(self):
        # self.query = query
        # self.query_type = query_type
        # self.vals = vals
        self.database = None
        self.cursor = None

    def db_connect(self):
        try:
            self.database = mysql.connector.connect(
                host=os.getenv("DATABASE_URL"),
                user=os.getenv("DATABASE_USER"),
                password=os.getenv("DATABASE_PASSWORD"),
                database=os.getenv("DATABASE_SCHEMA")
            )
            self.cursor = self.database.cursor(dictionary=True)
            print("database connected", self.database)
        except mysql.connector.Error as err:
            print(err)
    
    def db_book_query(self, query, date_time=None, query_vals=None, commit="false"):
        if self.database.is_connected():
                try:
                    self.cursor.execute(query, query_vals)

                    if commit:
                        self.database.commit()
                        self.cursor.execute("SELECT * FROM books b LEFT JOIN authors a ON b.books_author_id = a.authors_id WHERE b.books_date_added = %s", (date_time,))

                    response = self.cursor.fetchall()
                    data = []

                    for item in response:
                        book_object = {
                            "id": item["books_id"],
                            "title": item["books_title"],
                            "author": f"{item['authors_last_name']}, {item['authors_first_name']}",
                            "publication_year": item["books_pub_year"],
                            "isbn": item["books_isbn"],
                            "date_added": item["books_date_added"]
                        }

                        data.append(book_object)
                        
                    return data

                except mysql.connector.Error as err:
                    print("Something went wrong: {}".format(err))
                    return err

        else:
            print("database not connected")
            return "database not connected"

    def db_author_query(self, query, vals, commit):
        if self.database.is_connected():
            try:
                self.cursor.execute(query, vals)
                response = self.cursor.fetchall()

                data = []
                for author in response:
                    authorObject = {
                        "id": author['authors_id'],
                        "last_name": author['authors_last_name'],
                        "first_name": author['authors_first_name']
                    }
                    data.append(authorObject)
                
                return data
            except mysql.connector.Error as err:
                print("Something went wrong: {}".format(err))
                return err
        else:
            return "database not connected"

    def db_close(self):
        if self.database.is_connected():
            self.cursor.close()
            self.database.close()
            print("database connection closed")
        else:
            print("database not connected")