import time

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()


def read_card():
    card_id, text = reader.read()
    print(card_id, text)
    time.sleep(0.5)


if __name__ == "__main__":
    try:
        while 1:
            read_card()
    except KeyboardInterrupt:
        exit(1)
    finally:
        GPIO.cleanup()
