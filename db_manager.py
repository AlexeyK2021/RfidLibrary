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
                database="rfid_lib"
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

    def client_take_books(self, client_card_id, books_card_ids):  # Клиент получает книги
        query = """SELECT ChangeStatus(%s, %s);"""
        data = []

        for book in books_card_ids:
            data.append((client_card_id, book))

        self.connection.cursor().executemany(query, data)
        self.connection.cursor().close()
        self.connection.commit()

    def client_return_books(self, client_card_id, books_card_ids):  # Клиент возвращает книги. user_card_id = -1
        query = """SELECT ChangeStatus(%s, %s);"""
        data = []

        for book in books_card_ids:
            data.append((-1, book))

        self.connection.cursor().executemany(query, data)
        self.connection.cursor().close()
        self.connection.commit()
