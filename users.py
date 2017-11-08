from flask import current_app
#from passlib.apps import custom_app_context as pwd_context

class User:
    def __init__(self, name, surname, email, nickname, password):
        self.nickname = nickname
        self.hashed = hashing(password)
        self.name = name
        self.surname = surname
        self.email = email

    def get_id(self):
        return self.nickname

#def hashing(password):

    #return pwd_context.encrypt(password)
