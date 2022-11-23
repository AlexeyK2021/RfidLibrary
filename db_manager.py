import mysql.connector
from mysql.connector import Error

HOSTNAME = "194.87.239.99"
USERNAME = "alexey"
PASSWORD = "Alexey2002"


class db_manager:
    connection = None

    def __init__(self):
        self.create_connection(HOSTNAME, USERNAME, PASSWORD)

    def create_connection(self, hostname, username, password):
        try:
            self.connection = mysql.connector.connect(
                host=hostname,
                user=username,
                passwd=password,
                database="library"
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

    def getAll(self):
        show_db_query = "SELECT * FROM user_book;"
        with self.connection.cursor() as cursor:
            cursor.execute(show_db_query)
            for db in cursor:
                print(db)

    def client_take_books(self, client_card_id, books_card_ids):  # Клиент получает книги
        query = """INSERT INTO user_book(user_card_id, book_card_id, transaction_type) VALUES (%s, %s, 'take');"""
        data = []

        for book in books_card_ids:
            data.append((client_card_id, book))

        self.connection.cursor().executemany(query, data)
        self.connection.cursor().close()
        self.connection.commit()

    def client_return_books(self, client_card_id, books_card_ids):  # Клиент возвращает книги
        query = """INSERT INTO user_book(user_card_id, book_card_id, transaction_type) VALUES (%s, %s, 'return');"""
        data = []

        for book in books_card_ids:
            data.append((client_card_id, book))

        self.connection.cursor().executemany(query, data)
        self.connection.cursor().close()
        self.connection.commit()
