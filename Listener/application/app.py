from flask import Flask, request, session, g
from flask_restful import Api, Resource
from application.blueprints.routes import Users, Login, Register, Logout


# Initialize the flask api
app = Flask(__name__)
api = Api(app)
app.secret_key = "LDFKA\xdfgG;\xc3\xaf\x9fs\x9c\x99\x1dQS\xa8)\xff\xe4R\xc7\xf2\x05@y\xd2\xc1\xab\x0f\x99\xd8(\xd9Yal\xb6!x\x02q<^b?\x86\x08G\x8c\xbc\xf6\xc9n\x15\x0cDx\tUF\x83\x1a[\x10\xfd\x08\x16\xf5\xb3\xa6\xd0PR\xda\xf7\xf9\x1f\xa9#\xdfw\x0f&\xda:\x7f\xc5:@Z\x13\xf0FLw\r\x9aO\xc3\x8c\xbb7}\xd1\xdd\xdb\x05\x04\x11\x0c\xf3\x8a\x0bh\x13\xad\x16\x99k\x03Ji\x8b\x9e\xd3\xcf\xc8g\xc8SJGHTEAHBIODFBJN"

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None: db.close()


# Add resources to api
#api.add_resource(resources.HelloWorld, "/hello/<string:name>")
api.add_resource(Users, "/users/<string:username>")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(Register, "/register")