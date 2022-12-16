import time

from RPi import GPIO
from mfrc522 import SimpleMFRC522


def read_card(card_id, text):
    print(card_id, text)


def on_shutdown():
    GPIO.cleanup()
    exit(1)


if __name__ == "__main__":
    reader = SimpleMFRC522()
    while True:
        print(reader.read())

# user card ids: 584190577720, 388763356111
# books card ids: 584184339214, 584199150572, 584188336961, 584187943751, 584185977637
# stop card id: 1047968420567