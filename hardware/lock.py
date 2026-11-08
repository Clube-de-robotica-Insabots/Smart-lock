from time import sleep

from .rfid import Rfid
from .bolt import Bolt
import os as OS
from pathlib import Path

class Lock:
    def __init__(self, relay_a_pin, relay_b_pin, limit_switch_open_pin, limit_switch_close_pin):
        self._card_reader = Rfid()
        self._bolt = Bolt(relay_a_pin, relay_b_pin, limit_switch_open_pin, limit_switch_close_pin)

    def __unlock(self):
        self._bolt.open()

    def lock(self):
        self._bolt.close()

    def _relock_after_delay(self, delay):
        sleep(delay)
        self.lock()

    def try_unlock(self):
        pass

