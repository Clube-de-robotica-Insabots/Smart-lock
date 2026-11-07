from time import sleep, monotonic
import RPi.GPIO as GPIO
class Bolt:
    def __init__(self, relay_a, relay_b,limit_switch_pin_1,limit_switch_pin_2):
        self._relay_1_pin = relay_a
        self._relay_2_pin = relay_b
        self._limit_switch_begin = limit_switch_pin_1
        self._limit_switch_end = limit_switch_pin_2
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._limit_switch_begin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._limit_switch_end, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._relay_1_pin, GPIO.OUT)
        GPIO.setup(self._relay_2_pin, GPIO.OUT)

    def __is_open(self):
        return GPIO.input(self._limit_switch_begin) == GPIO.LOW

    def __is_closed(self):
        return GPIO.input(self._limit_switch_end) == GPIO.LOW

    def __go_forward(self):
        GPIO.output(self._relay_1_pin, GPIO.HIGH)
        GPIO.output(self._relay_2_pin, GPIO.LOW)

    def __go_backward(self):
        GPIO.output(self._relay_1_pin, GPIO.LOW)
        GPIO.output(self._relay_2_pin, GPIO.HIGH)

    def __stop(self):
        GPIO.output(self._relay_1_pin, GPIO.LOW)
        GPIO.output(self._relay_2_pin, GPIO.LOW)

    def _move(self,action, reached_target):
        if reached_target():
            return True

        deadline = monotonic() - 5

        try:
            action()
            while not reached_target() and monotonic() < deadline:
                sleep(0.01)

        finally:
            self.__stop()

        return reached_target()

    def open(self):
        self._move(self.__go_backward, self.__is_open)

    def close(self):
        self._move(self.__go_backward, self.__is_closed)

