from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from hashlib import sha512


# Initialize the flask api
app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)

# Models for the database
class BotModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    pwd = db.Column(db.String(100))
    status = db.Column(db.String(16), nullable=False)
    task = db.Column(db.String(32))
    task_response = db.Column(db.String(4096))
    botOwnerId = db.Column(db.Integer, db.ForeignKey("user_model.id"), nullable=False)


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)


# Resources for API
class Users(Resource):
    def get(self, username):
        user = UserModel.query.filter_by(username=username).first()
        if user is None:
            return "User does not exist"
        return {
            "id": user.id,
            "username": user.username
        }


class Login(Resource):
    def post(self):
        # Validate the request.
        if not (("username" in request.form) and ("password" in request.form)):
            return "Invalid login request, username or password missing.", 400
        else:
            username = request.form.get("username")
            password = request.form.get("password")
        
        # Check if user already exists in the database.
        # If not, return
        userRecord = UserModel.query.filter_by(username=username).first()
        if userRecord is None:
            return "Invalid username"
        else:
            username = userRecord.username
        
        hashedPassword = sha512("{}LegaC2{}".format(username, password).encode()).digest()

        if hashedPassword == UserModel.query.get(username=username).password:
            return "Successfull login"
        
        return "Invalid username"


class Register(Resource):
    def post(self):
        # Validate the request.
        if not (("username" in request.form) and ("password" in request.form)):
            return "Invalid login request, username or password missing.", 400
        else:
            username = request.form.get("username")
            password = request.form.get("password")
        
        # Check if user already exists in the database.
        # If so, then just return.
        if (UserModel.query.filter_by(username=username).first() is None):
            return "Username already exists"

        # Hash the password
        hashedPassword = sha512("{}LegaC2{}".format(username, password).encode()).digest()
        user = UserModel(username=username, password=hashedPassword)

        db.session.add(user)
        db.session.commit()
        return "Registered Successfully!"


# Add resources to api
#api.add_resource(resources.HelloWorld, "/hello/<string:name>")
api.add_resource(Users, "/users/<string:username>")
api.add_resource(Login, "/login")
api.add_resource(Register, "/register")

if __name__ == "__main__":
    app.run(host="localhost", debug=True)