from application.database import query_db
from hashlib import sha256

class users(object):

    @staticmethod
    def add(username, password):
        query_db("INSERT INTO user (username, password) VALUES (?, ?)", [username, password])
        return True

    @staticmethod
    def username_exists(username):
        return len(query_db("SELECT 1 FROM user WHERE username=?", [username])) == 1

    @staticmethod
    def user_exists(username, password):
        return len(query_db("SELECT 1 FROM user WHERE username=? and password=?", [username, password])) == 1
    
    @staticmethod
    def get_user(username):
        return query_db("SELECT * FROM user WHERE username=?", [username])