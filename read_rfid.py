import time

import RPi.GPIO as GPIO
from mfrc522 import MFRC522

import work_state
from rfid_reader import rfid_reader
from db_manager import db_manager

scanned_data_ids = []
client_card_id = 0
books_ids = []
global db, ws


def read_card(card_id, text):
    global client_card_id, books_ids
    print(card_id, text)
    if card_id == client_card_id and len(books_ids) > 0:
        end_transaction()
        return

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
    if ws.curr_state == ws.take_book:
        db.client_take_books(client_card_id, books_ids)
    elif ws.curr_state == ws.return_book:
        db.client_return_books(client_card_id, books_ids)

    ws.curr_state = ws.waiting
    client_card_id = 0
    books_ids.clear()
    scanned_data_ids.clear()
    print("Waiting next card")


def gpio_handling():
    try:
        while ws.curr_state != ws.off:
            if GPIO.input(23) and GPIO.input(24):
                ws.switch_off()
            elif GPIO.input(23):
                ws.take_button()
            elif GPIO.input(24):
                ws.return_button()
            elif ws.curr_state != ws.waiting:
                rfid.read_rfid_card_forever_loop()
            switch_leds()
            print(ws.curr_state)
            time.sleep(0.5)
        on_shutdown()
    except KeyboardInterrupt:
        on_shutdown()


def switch_leds():
    if ws.curr_state == ws.take_book:
        GPIO.output(27, GPIO.LOW)
        GPIO.output(17, GPIO.HIGH)
    elif ws.curr_state == ws.return_book:
        GPIO.output(17, GPIO.LOW)
        GPIO.output(27, GPIO.HIGH)
    elif ws.curr_state == ws.waiting:
        GPIO.output(17, GPIO.LOW)
        GPIO.output(27, GPIO.LOW)


def setup():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN)
    GPIO.setup(24, GPIO.IN)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)


def on_shutdown():
    show_all_cards()
    GPIO.output(17, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
    GPIO.cleanup()
    exit(1)


def show_all_cards():
    print("client_card_id is", client_card_id, "\nbook_ids are", *books_ids, end="\n")


if __name__ == "__main__":
    setup()
    ws = work_state.work()
    rfid = rfid_reader(ws)
    db = db_manager()
    rfid.on_new_card_read = read_card
    rfid.on_shutdown = on_shutdown
    gpio_handling()
