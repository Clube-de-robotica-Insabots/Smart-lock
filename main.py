from time import sleep
from auth.user_repository import UserRepository
from auth.card_auth import CardAuthenticator
from lock import Lock

RELAY_A_PIN = 4
RELAY_B_PIN = 5
LIMIT_SWITCH_OPEN_PIN = 6
LIMIT_SWITCH_CLOSE_PIN = 7
USERS_FILE_PATH = "data/users.json"
user_repo = UserRepository(USERS_FILE_PATH)
auth = CardAuthenticator(user_repo)
lock = Lock(RELAY_A_PIN, RELAY_B_PIN, LIMIT_SWITCH_OPEN_PIN, LIMIT_SWITCH_CLOSE_PIN)

if __name__ == "__main__":
    while True:
        lock.try_unlock()
        sleep(0.1)