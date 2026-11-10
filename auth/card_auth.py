class CardAuthenticator:
    def __init__(self, user_repository):
        self._user_repository = user_repository

    def is_authorized(self, uid):
        user = self._user_repository.find_by_uid(uid)
        if user is None or not user.active:
            return False
        else:
            return True