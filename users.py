import flask_login
from passlib.apps import custom_app_context as pwd_context
login_manager = flask_login.LoginManager()

class User(flask_login.UserMixin):
    def __init__(self, name, surname, email, nickname, password):
        self.nickname = nickname
        self.password = hashing(password)
        self.name = name
        self.surname = surname
        self.email = email
        self.authenticated = True

    def get_id(self):
        return self.nickname

    def is_authenticated(self):
        return self.authenticated

    @property
    def is_active(self):
        return True

def hashing(password):
    secret_key = 'helloworld'
    return pwd_context.encrypt(password)
