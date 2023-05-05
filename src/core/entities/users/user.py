

class User(object):
    def __init__(self, user_id: str, username: str, fullname: str):
        self._user_id = user_id
        self._username = username
        self._fullname = fullname

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id_value):
        self._user_id = user_id_value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username_value):
        self._username = username_value

    @property
    def fullname(self):
        return self._fullname

    @fullname.setter
    def fullname(self, fullname_value):
        self._fullname = fullname_value
