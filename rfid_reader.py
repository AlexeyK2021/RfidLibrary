import time

from mfrc522 import SimpleMFRC522


class rfid_reader:
    reader = SimpleMFRC522()
    on_new_card_read = None
    on_shutdown = None

    def read_rfid_card_forever_loop(self):
        text = ""
        while not text.startswith("stop"):
            card_id, text = self.reader.read()
            self.on_new_card_read(card_id, text)
            time.sleep(0.5)
        self.on_shutdown()
