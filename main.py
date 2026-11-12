import signal
import sys
from time import sleep

from auth.user_repository import UserRepository
from auth.card_auth import CardAuthenticator
from lock import Lock

RELAY_A_PIN = 15  # GPIO22
RELAY_B_PIN = 13  # GPIO27
LIMIT_SWITCH_OPEN_PIN = 16  # GPIO23
LIMIT_SWITCH_CLOSE_PIN = 18  # GPIO24
USERS_FILE_PATH = "data/users.json"
CARD_POLL_INTERVAL_SECONDS = 0.1


def stop_service(signum, frame):
    # O systemd encerra o serviço com SIGTERM. Por padrão o Python morre na
    # hora, sem rodar os blocos finally; o sys.exit faz eles rodarem, o que
    # garante que o motor pare e os pinos sejam liberados.
    sys.exit(0)


def main():
    signal.signal(signal.SIGTERM, stop_service)

    user_repository = UserRepository(USERS_FILE_PATH)
    authenticator = CardAuthenticator(user_repository)
    lock = Lock(RELAY_A_PIN, RELAY_B_PIN, LIMIT_SWITCH_OPEN_PIN, LIMIT_SWITCH_CLOSE_PIN, authenticator)

    try:
        while True:
            lock.try_unlock()
            sleep(CARD_POLL_INTERVAL_SECONDS)
    finally:
        lock.cleanup()


if __name__ == "__main__":
    main()
