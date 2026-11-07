from time import sleep, monotonic
import RPi.GPIO as GPIO
class BoltJammedError(Exception):
    pass

RELAY_ON = GPIO.HIGH
RELAY_OFF = GPIO.LOW
TIMEOUT_SECONDS = 5
SLEEP_SECONDS = 0.01

class Bolt:
    def __init__(self, relay_a, relay_b, limit_switch_pin_1, limit_switch_pin_2):
        self._relay_1_pin = relay_a
        self._relay_2_pin = relay_b
        self._limit_switch_open = limit_switch_pin_1
        self._limit_switch_closed = limit_switch_pin_2
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._limit_switch_open, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._limit_switch_closed, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._relay_1_pin, GPIO.OUT)
        GPIO.setup(self._relay_2_pin, GPIO.OUT)

    def is_open(self):
        return GPIO.input(self._limit_switch_open) == GPIO.LOW

    def is_closed(self):
        return GPIO.input(self._limit_switch_closed) == GPIO.LOW

    def __go_forward(self):
        GPIO.output(self._relay_1_pin, RELAY_ON)
        GPIO.output(self._relay_2_pin, RELAY_OFF)

    def __go_backward(self):
        GPIO.output(self._relay_1_pin, RELAY_OFF)
        GPIO.output(self._relay_2_pin, RELAY_ON)

    def __stop(self):
        GPIO.output(self._relay_1_pin, RELAY_OFF)
        GPIO.output(self._relay_2_pin, RELAY_OFF)

    def __wait_until(self, reached_target):
        deadline = monotonic() + TIMEOUT_SECONDS
        while not reached_target() and monotonic() < deadline:
            sleep(SLEEP_SECONDS)

    def __move(self,action, reached_target):
        if reached_target():
            return
        try:
            action()
            self.__wait_until(reached_target)
        finally:
            self.__stop()

        if not reached_target():
            raise BoltJammedError("The Bolt is jammed!")

    def open(self):
        self.__move(self.__go_backward, self.is_open)

    def close(self):
        self.__move(self.__go_forward, self.is_closed)

