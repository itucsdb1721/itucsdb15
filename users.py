from flask import current_app
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, name, surname, email, nickname, password):
        self.nickname = nickname
        self.password = password
        self.name = name
        self.surname = surname
        self.email = email

    def get_id(self):
        return self.nickname
