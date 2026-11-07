import RPi.GPIO as GPIO
class Bolt:
    def __init__(self, relay_a, relay_b,limit_switch_pin_1,limit_switch_pin_2):
        self._relay_1_pin = relay_a
        self._relay_2_pin = relay_b
        self._limit_switch_begin = limit_switch_pin_1
        self._limit_switch_end = limit_switch_pin_2
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._limit_switch_begin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._limit_switch_end, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._relay_1_pin, GPIO.OUT)
        GPIO.setup(self._relay_2_pin, GPIO.OUT)

    def __is_open(self):
        return GPIO.input(self._limit_switch_begin) == GPIO.LOW

    def __is_closed(self):
        return GPIO.input(self._limit_switch_end) == GPIO.LOW

    def abrir(self):
        GPIO.output(self._relay_1_pin, GPIO.HIGH)
        GPIO.output(self._relay_2_pin, GPIO.LOW)

    def fechar(self):
        GPIO.output(self._relay_1_pin, GPIO.LOW)
        GPIO.output(self._relay_2_pin, GPIO.HIGH)
