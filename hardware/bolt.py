import RPi.GPIO as GPIO
class Bolt:
    def __init__(self, relay_a, relay_b,limit_switch_pin_1,limit_switch_pin_2):
        self._relay_1_pin = port1
        self._relay_2_pin = port2
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._relay_1_pin, GPIO.OUT)
        GPIO.setup(self._relay_2_pin, GPIO.OUT)

    def abrir(self):
        GPIO.output(self._relay_1_pin, GPIO.HIGH)
        GPIO.output(self._relay_2_pin, GPIO.LOW)

    def fechar(self):
        GPIO.output(self._relay_1_pin, GPIO.LOW)
        GPIO.output(self._relay_2_pin, GPIO.HIGH)
