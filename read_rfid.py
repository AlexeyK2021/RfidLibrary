import RPi.GPIO as GPIO

from rfid_reader import rfid_reader
from db_manager import db_manager

scanned_data_ids = []
client_card_id = 0
books_ids = []
global db


def read_card(card_id, text):
    print(card_id, text)
    if card_id == client_card_id and len(books_ids) > 0:
        end_transaction()

    if card_id not in scanned_data_ids:
        scanned_data_ids.append(card_id)

    process_data()


def process_data():
    global client_card_id, books_ids
    client_card_id = scanned_data_ids[0]
    books_ids = scanned_data_ids[1:]


def end_transaction():
    global client_card_id, books_ids
    process_data()
    show_all_cards()
    db.client_take_books(client_card_id, books_ids)
    client_card_id = 0
    books_ids = []
    print("Waiting next card")


def on_shutdown():
    process_data()
    show_all_cards()

    GPIO.cleanup()
    exit(1)


def show_all_cards():
    print("client_card_id is", client_card_id, "\nbook_ids are", *books_ids, end="\n")


if __name__ == "__main__":
    rfid = rfid_reader()
    db = db_manager()
    rfid.on_new_card_read = read_card
    rfid.on_shutdown = on_shutdown
    rfid.read_rfid_card_forever_loop()
