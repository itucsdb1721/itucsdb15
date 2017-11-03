class Users:
    def __init__(self):
        self.users = {}
        self.last_user_id = 0

    def add_user(self, user):
        self.last_user_id += 1
        self.users[self.last_user_id] = user
        user._id = self.last_user_id

    def delete_user(self, user_id):
        del self.users[user_id]

    def get_user(self, user_id):
        return self.users[user_id]

    def get_users(self):
        return self.users