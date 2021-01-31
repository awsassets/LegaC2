from flask import request, session
from flask_restful import Resource
from application.models import users
from hashlib import sha512


def loggedIn():
    if "username" in session:
        return True

    return False


# Resources for API
class Users(Resource):
    def get(self, username):
        user = users.get_user(username)
        if not user:
            return {
                "id": None,
                "username": None
            }
        user = user[0]
        return {
            "id": user["id"],
            "username": user["username"]
        }


class Login(Resource):
    def post(self):
        # Validate the request.
        if not (("username" in request.form) and ("password" in request.form)):
            return "Invalid login request, username or password missing.", 400
        else:
            username = request.form.get("username")
            password = request.form.get("password")
        
        # Check if the user is already logged in
        if loggedIn():
            return "Already logged in as {0}".format(session["username"])

        # Calculate the password hash, and if the record with that specific username exists
        hashedPassword = sha512(password.encode("utf-8")).hexdigest()
        if users.user_exists(username, hashedPassword):
            session["username"] = username
            return "Logged in successfully"

        return "Invalid username/password combination"


class Logout(Resource):
    def get(self):
        if not "username" in session:
            return "Not logged in"
        
        session.pop("username", None)
        return "Logged out successfully"


class Register(Resource):
    def post(self):
        # Validate the request.
        if not (("username" in request.form) and ("password" in request.form)):
            return "Invalid login request, username or password missing.", 400
        else:
            username = request.form.get("username")
            password = request.form.get("password")
        
        # Check if the user is already logged in
        if loggedIn():
            return "Already logged in as {0}".format(session["username"])

        # Check if user already exists in the database.
        # If so, then just return.
        if users.username_exists(username):
            return "Username already exists"

        # Hash the password
        hashedPassword = sha512(password.encode("utf-8")).hexdigest()
        users.add(username, hashedPassword)
        return "Registered Successfully!"