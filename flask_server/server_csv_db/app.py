from typing import Dict, List, Union

from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

users = []


def read_from_file():
    global users
    users = []  # type: List[Dict[str, Union[str, int]]]
    f = open("db.csv", "r")
    linhas = f.read()
    linhas = linhas.split("\n")
    linhas = linhas[:-1]
    for i in linhas:
        x = i.split(',')
        objct = {
            "name": str(x[0]),
            "age": int(x[1]),
            "occupation": str(x[2])
        }
        # print(dict)
        users.append(objct)


def write_to_file():
    f = open("db.csv", "w")
    for i in users:
        put_to_file(i, f)


def put_to_file(i, f):
    f.write(str(i['name']) + ',' + str(i['age']) + ',' + str(i['occupation']) + '\n')


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
        write_to_file()
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
        write_to_file()
        return user, 201

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        global users
        users = [user for user in users if user["name"] != args["name"]]
        write_to_file()
        return "{} is deleted.".format(args["name"]), 200


class List_Users(Resource):
    def get(self):
        global users
        read_from_file()

        return users, 200


class RereadBD(Resource):
    def get(self):
        global users
        users = []
        return "Reread made successfully"


api.add_resource(User, "/user/rud")
api.add_resource(List_Users, "/user/list")
api.add_resource(RereadBD, "/user/rereadBD")

read_from_file()
app.run(debug=True)
