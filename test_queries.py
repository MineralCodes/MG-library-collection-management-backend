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


#saved logic from DatabaseConnection class

# def db_book_query(self, query, date_time=None, query_vals=None, commit=False):
#         if self.database.is_connected():
#                 try:
#                     self.cursor.execute(query, query_vals)

#                     if commit:
#                         self.database.commit()
#                         self.cursor.execute("SELECT * FROM books b LEFT JOIN authors a ON b.books_author_id = a.authors_id WHERE b.books_date_added = %s", (date_time,))

#                     response = self.cursor.fetchall()

#                     res_object = self.generate_response_object(response, "book")
#                     # data = []

#                     # for item in response:
#                     #     book_object = {
#                     #         "id": item["books_id"],
#                     #         "title": item["books_title"],
#                     #         "author": f"{item['authors_last_name']}, {item['authors_first_name']}",
#                     #         "publication_year": item["books_pub_year"],
#                     #         "isbn": item["books_isbn"],
#                     #         "date_added": item["books_date_added"]
#                     #     }

#                     #     data.append(book_object)
                        
#                     return res_object

#                 except mysql.connector.Error as err:
#                     print("Something went wrong: {}".format(err))
#                     return err

#         else:
#             print("database not connected")
#             return "database not connected"

#     def db_author_query(self, query, commit=False, vals=None):
#         if self.database.is_connected():
#             try:
#                 self.cursor.execute(query, vals)
#                 if commit:
#                     self.database.commit()
#                     self.cursor.execute("SELECT * FROM authors WHERE authors_last_name = %s AND authors_first_name = %s", vals)
                
#                 response = self.cursor.fetchall()

                
#                 data = []
#                 for author in response:
                    
#                     data.append(authorObject)
                
#                 return data


#             except mysql.connector.Error as err:
#                 print("Something went wrong: {}".format(err))
#                 return err
#         else:
#             return "database not connected"

# def db_user_auth(self, query, vals=None):
#         if self.database.is_connected():
#             self.cursor.execute(query, vals)
            
#             results = self.cursor.fetchall()

#             content = []

#             for result in results:
#                 content.append(result)
        
#         return content[0]