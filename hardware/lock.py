from .rfid import Rfid
from .bolt import Bolt

class Lock:
    def __init__(self, relay_a_pin, relay_b_pin, limit_switch_open_pin, limit_switch_close_pin):
        self._card_reader = Rfid()
        self._bolt = Bolt(relay_a_pin, relay_b_pin, limit_switch_open_pin, limit_switch_close_pin)

