import json
from pathlib import Path
from .user import User

class UserRepository:
    def __init__(self, file_path):
        self._file_path = Path(file_path)

    def _load_users(self):
        users = []
        with open(self._file_path, 'r', encoding='UTF-8') as file:
            users_data = json.load(file)
        for user_data in users_data:
            new_user = User(**user_data)
            users.append(new_user)
        return users

    def find_by_uid(self, uid):
        users = self._load_users()
        for user in users:
            if user.uid == uid:
                return user
        return None


