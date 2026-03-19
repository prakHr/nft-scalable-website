
from flask_login import UserMixin

# Simple in-memory user store
USERS = {}

class User(UserMixin):
    def __init__(self, username):
        self.id = username
        

    @staticmethod
    def validate_login(username, password):
        return USERS.get(username) == password
