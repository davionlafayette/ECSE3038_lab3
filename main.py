from flask import Flask, request, jsonify, json
from flask_pymongo import PyMongo 
from marshmallow import Schema, fields, ValidationError
from bson.json_util import dumps
from json import loads
from datetime import datetime



app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://eramiskell:fallenhippo@cluster0.tjzit.mongodb.net/Lab3?retryWrites=true&w=majority"
mongo = PyMongo(app)



profile = {
    "data":{"last_updated": "2/3/2021, 8:48:51 PM", 
            "username": "Jimmy_Woo",
            "role": "Engineer",
            "color": "green"
            }
}

tank_info = []
tank_id = 0

class TankSchema(Schema):
    location = fields.String(required=True)
    latitude  = fields.String(required=True)
    longitude = fields.String(required=True)
    percentage_full = fields.Integer(required=True)

@app.route("/")
def home():
    return "Hello There"

@app.route("/profile", methods=["GET"])
def get_profile():
    return profile


@app.route("/profile", methods=["POST"])
def post_profile():
    profile["username"] = request.json["username"]
    profile["role"] = request.json["role"]
    profile["color"] = request.json["color"]
    profile["last_updated"] = datetime.now()

    return{
        "success": True,
        "data": profile
    }

@app.route("/profile", methods=["PATCH"])
def update_profile():
    if "username" in request.json:
        profile["username"] = request.json["username"]
  
    if "role" in request.json:
        profile["role"] = request.json["role"]

    if "color" in request.json:
        profile["color"] = request.json["color"]
  
    profile["last_updated"] = datetime.now()

    return {
        "success": True,
        "data": profile
    }

#GET /data
@app.route("/data", methods=["GET"])
def get_tank():
    tanks = mongo.db.tanks.find()
    return jsonify(loads(dumps(tanks)))

@app.route("/data", methods=["POST"])
def add_tank():
    try:
        newTank = TankSchema().load(request.json)
        tank_id = mongo.db.tanks.insert_one(newTank).inserted_id
        tank = mongo.db.tanks.find_one(tank_id)
        return loads(dumps(tank))
    except ValidationError as ve:
        return ve.messages, 400

@app.route("/data/<ObjectID:id>", methods=["PATCH"])
def update_tank(id):
    mongo.db.tanks.update_one(({"_id": id}), {"$set": request.json})
    tank = mongo.db.tanks.find_one(id)
    return loads(dumps(tank))

@app.route("/data/<ObjectId:id>", methods=["DELETE"])
def delete_tank(id):
    result = mongo.db.fruits.delete_one({"_id": id})
    if result.deleted_count == 1:
        return{
            "success": True
        }
    else:
        return{
            "success": False
        }, 400

if __name__ == "__main__":
    app.run(debug=True)
