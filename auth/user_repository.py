import json
from pathlib import Path
from .user import User

class DuplicateUserError(Exception):
    pass

class UserNotFound(Exception):
    pass

class UserRepository:
    def __init__(self, file_path):
        self._file_path = Path(file_path)

    def _load_users(self):
        users = []
        with open(self._file_path, 'r', encoding='UTF-8') as file:
            users_data = json.load(file)
        for user_data in users_data:
            user = User(**user_data)
            users.append(user)
        return users

    def list_all(self):
        return self._load_users()

    def find_by_uid(self, uid):
        users = self._load_users()
        for user in users:
            if user.uid == uid:
                return user
        return None

    def add(self, user):
        if self.find_by_uid(user.uid) is not None:
            raise DuplicateUserError("Cannot add user: a user with this UID already exists in the registry.")
        else:
            with open(self._file_path, 'r', encoding='UTF-8') as file:
                users_data = json.load(file)
            new_user = vars(user)
            users_data.append(new_user)
            with open(self._file_path, 'w', encoding='UTF-8') as file:
                json.dump(users_data, file, indent=2, ensure_ascii=False)

    def remove(self, user):
        if self.find_by_uid(user.uid) is None:
            raise UserNotFound("The user you tried to delete was not found!")
        else:
            with open(self._file_path, 'r', encoding='UTF-8') as file:
                users_data = json.load(file)
            list_of_users = [user_data for user_data in users_data
                                if user_data["uid"] != user.uid]
            with open(self._file_path, 'w', encoding='UTF-8') as file:
                json.dump(list_of_users, file, indent=2, ensure_ascii=False)






