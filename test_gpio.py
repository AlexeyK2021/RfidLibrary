import time

from RPi.GPIO import GPIO


def blink():
    GPIO.output(7, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(7, GPIO.LOW)
    time.sleep(1)


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)
    GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def loop():
    blink()
    if GPIO.input(11):
        return False
    return True


def reset():
    GPIO.cleanup()


if __name__ == "__main__":
    setup()
    isWork = True
    while isWork:
        isWork = loop()
    reset()
