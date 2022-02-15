from marshmallow import Schema, fields, ValidationError
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
from datetime import datetime
from flask_cors import CORS
from json import loads
import pandas as pd

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb+srv://<Osiris>:<FPid9itnygVzFvk1>@cluster0.tjzit.mongodb.net/lab3?retryWrites=true&w=majority"
mongo = PyMongo(app)

profile = {
    "success": True,
    "data":{"last_updated": "2/3/2021, 8:48:51 PM",
            "username": "Jimmy_Woo",
            "role": "Engineer",
            "color": "green"
            }
}

class TanksSchema(Schema):
    location = fields.String(required=True)
    latitude  = fields.String(required=True)
    longitude = fields.String(required=True)
    percentage_full = fields.Integer(required=True)

@app.route("/")
def home():
    return "ECSE3038 Lab 3"

@app.route("/profile", methods=["GET", "POST", "PATCH"])
def getting_profile():
    if request.method == "GET":
        return jsonify(Profile)

    elif request.method == "POST":
        now = datetime.now()
        datetimee = now.strftime("%d/%m/%Y %H:%M:%S")

        Profile["data"]["last_updated"] = (datetimee)
        Profile["data"]["username"] = (request.json["username"])
        Profile["data"]["role"] = (request.json["role"])
        Profile["data"]["color"] = (request.json["color"])

        return jsonify(Profile)

    elif request.method == "PATCH":
        now = datetime.now()
        datetimee = now.strftime("%d/%m/%Y %H:%M:%S")
    
        data = Profile["data"]

        r = request.json
        r["last_updated"] = datetimee
        attributes = r.keys()
        for attribute in attributes:
            data[attribute] = r[attribute]

        return jsonify(Profile)      

@app.route("/data", methods=["GET", "POST"])
def tank_data():
    if request.method == "GET":
        Tanks = mongo.db.Tanks.find()
        return jsonify(loads(dumps(Tanks)))

    elif request.method == "POST":
        try:
            Tank = TanksSchema().load(request.json)
            mongo.db.Tanks.insert_one(Tank)
            return loads(dumps(Tank))
        except ValidationError as ve:
            return ve.messages, 400 

@app.route('/data/<ObjectId:id>', methods=["PATCH", "DELETE"])
def tank_id_methods(id):
    if request.method == "PATCH":

        mongo.db.Tanks.update_one({"_id": id}, {"$set": request.json})
        Tank = mongo.db.tanks.find_one(id)
        return jsonify(Tank)
        return loads(dumps(Tank))

    elif request.method == "DELETE":
        result = mongo.db.Tanks.delete_one({"_id": id})

        if result.deleted_count == 1:
            return {"success": True}
        else:
            return {"success": False}, 400

if __name__ == "__main__":
    app.run( debug=True,port =3000, host = "0.0.0.0")
