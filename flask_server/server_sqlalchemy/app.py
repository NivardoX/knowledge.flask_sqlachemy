from typing import Dict, List, Union
from flask import Flask, render_template, request
from flask_restful import Api, Resource, reqparse
import os
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "peopledatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)
api = Api(app)

users = []


class User_dba(db.Model):
    name = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    occupation = db.Column(db.String(80), nullable=True)

    def __repr__(self):
        return "<Nome: {} , Idade: {} , Profissão: {}>".format(self.title, self.age, self.occupation)

class User_object:
    def __init__(self, name,age,occupation):
        self.name = name
        self.age = age
        self.occupation = occupation

class User(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if args["name"] == user["name"]:
                return user, 200

        return "User not found", 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if args["name"] == user["name"]:
                return "User with name {} already exists".format(args["name"]), 400

        user = {
            "name": args["name"],
            "age": args["age"],
            "occupation": args["occupation"]
        }
        users.append(user)

        return user, 201

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if args["name"] == user["name"]:
                user["age"] = args["age"]
                user["occupation"] = args["occupation"]
                return user, 200

        user = {
            "name": args["name"],
            "age": args["age"],
            "occupation": args["occupation"]
        }
        users.append(user)
        return user, 201

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        global users
        users = [user for user in users if user["name"] != args["name"]]
        return "{} is deleted.".format(args["name"]), 200


class List_Users(Resource):
    def get(self):
        global users

        return users, 200


class RereadBD(Resource):
    def get(self):
        global users
        users = []
        return "Reread made successfully"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        user = User_dba(name = request.form.get("name"), age = request.form.get("age"), occupation = request.form.get("occupation"))
        db.session.add(user)
        db.session.commit()
        users = User_dba.query.all()
        return render_template("home.html",users=users)

    users = User_dba.query.all()
    return render_template("home.html",users=users)

if __name__ == "__main__":
    api.add_resource(User, "/user/rud")
    api.add_resource(List_Users, "/user/list")
    api.add_resource(RereadBD, "/user/rereadBD")

    app.run(debug=True)
