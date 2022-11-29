import time

from mfrc522 import SimpleMFRC522

import work_state


class rfid_reader:
    reader = SimpleMFRC522()
    on_new_card_read = None
    ws = None

    def __init__(self, ws):
        self.ws = ws

    def read_rfid_card_forever_loop(self):  # Зависает чтение карты
        text = ""
        card_id, text = self.reader.read()
        if text.startswith("stop"):
            self.ws.switch_waiting()
            return
        self.on_new_card_read(card_id, text)
