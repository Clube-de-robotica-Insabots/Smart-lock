import logging
from time import sleep
from hardware.rfid import Rfid
from hardware.bolt import Bolt

RELOCK_DELAY_SECONDS = 5


class Lock:
    def __init__(self, relay_a_pin, relay_b_pin, limit_switch_open_pin, limit_switch_close_pin, authenticator):
        self._card_reader = Rfid()
        self._bolt = Bolt(relay_a_pin, relay_b_pin, limit_switch_open_pin, limit_switch_close_pin)
        self._authenticator = authenticator

    def __unlock(self):
        self._bolt.open()

    def lock(self):
        self._bolt.close()

    def _relock_after_delay(self, delay):
        sleep(delay)
        self.lock()

    def try_unlock(self):
        uid = self._card_reader.read_uid()
        if uid is None:
            return False
        elif self._authenticator.is_authorized(uid):
            self.__unlock()
            self._relock_after_delay(RELOCK_DELAY_SECONDS)
            logging.warning(f"Acesso concedido: {uid}")
            return True
        else:
            logging.warning(f"Acesso negado: {uid}")
            return False

    def cleanup(self):
        # Para o motor e devolve os pinos, mesmo se uma das etapas falhar.
        try:
            self._bolt.cleanup()
        finally:
            self._card_reader.close()

