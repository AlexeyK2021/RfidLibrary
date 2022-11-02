from rfid_reader import rfid_reader


def read_card(card_id, text):
    print(card_id, text)


if __name__ == "__main__":
    rfid = rfid_reader()
    rfid.on_new_card_read = read_card
    rfid.read_rfid_card_forever_loop()

