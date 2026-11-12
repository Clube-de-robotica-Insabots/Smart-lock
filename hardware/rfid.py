from mfrc522 import SimpleMFRC522
class Rfid:
    def __init__(self):
        self._reader = SimpleMFRC522()

    def read_uid(self):
        return self._reader.read_id_no_block()

    def close(self):
        # Fecha a conexão SPI e libera o pino de reset do leitor.
        self._reader.READER.Close_MFRC522()
