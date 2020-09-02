from bson import ObjectId
from datetime import datetime
import pytz
from flask import request, jsonify, make_response
from database.db_config import mongo
from http import HTTPStatus as status
from flask_restful import abort
from bcrypt import checkpw, hashpw, gensalt
import json
from flask import Blueprint
from flask_jwt_extended import jwt_required, create_access_token


user_routes = Blueprint("user_routes", __name__, url_prefix="/user")
db = mongo.get_database("testcart").get_collection("users")


@user_routes.route("/modify", methods=["POST"])
def modify():
    data = json.loads(request.get_data())
    user_id = data.get("user_id", "")
    image = data.get("image", None)
    name = data.get("name", "No name")
    update = {"name": name, "image": image} if image else {"name": name}
    
    user = db.find_one_and_update({"_id":ObjectId(user_id)}, {"$set": update},{"password":0})
    return jsonify({
        "message": "Profile Update",
        "user": user
    }), status.OK
    
    
@user_routes.route("/forgot", methods=["POST"])
def forgot():
    data = json.loads(request.get_data())
    username = data.get('username')
    email = data.get('email')
    name = data.get('name')
    new_password = data.get('new_password')
    
    hashedPassword = hashpw(bytes(new_password, "utf-8"), gensalt())
    user = db.find_one_and_update({"username":username},{"$set":{"password":hashedPassword}},{"password":0})
    
    return jsonify({
        "message": "Profile Update",
        "user": user
    }), status.OK
        


@user_routes.route("/signup", methods=["POST"])
def signup():
    data = json.loads(request.get_data())
    email = data.get("email", None)
    user = db.find_one({"email": email})
    if user:
        return jsonify({"message": "User already exist"}), status.CONFLICT

    else:
        hashedPassword = hashpw(bytes(data.get("password", None), "utf-8"), gensalt())
        joined = datetime.now(pytz.timezone("Asia/Kolkata")).strftime(
            "%a, %-I:%M %p,  %-d %B, %Y"
        )
        user = db.insert_one(
            {
                "name": data.get("name", ""),
                "email": email,
                "password": hashedPassword,
                "username": data.get("username", ""),
                "favorites": [],
                "address": [],
                "orders": [],
                "cards": [],
                "joined": joined,
            }
        )
        return jsonify({"message": "User registeration successful"}), status.CREATED


@user_routes.route("/login", methods=["POST"])
def login():
    data = json.loads(request.get_data())
    username = data.get("username", None)
    password = data.get("password", None)

    user = db.find_one({"username": username})
    if user:    
        if checkpw(bytes(password, "utf-8"), user["password"]):
            token = create_access_token(identity=[username], expires_delta=False)
            del user["password"]
            return (
                jsonify(
                    {"token": token, "message": "Authentication Success", "user": user}
                ),
                status.ACCEPTED,)
        return jsonify({"message": "Incorrect password"}), status.NOT_FOUND
        # abort(http_status_code=status.NOT_FOUND, message="Incorrect password")
    return jsonify({"message": "Incorrect username"}), status.NOT_FOUND

        
@user_routes.route("/favorite", methods=["POST"])
@jwt_required
def addFavorite():
    data = json.loads(request.get_data())

    new_favorite = data.get("favorite", None)
    user_id = data.get("user_id", None)

    if user_id:
        user_id = ObjectId(user_id)
    else:
        return jsonify({"message": "No user"}), status.NOT_FOUND

    user = db.update_one({"_id": user_id}, {"$set": {"favorites": new_favorite}})
    print(user)
    if user.matched_count and user.modified_count == 0:

        return jsonify({"message": "Updated"}), status.OK
    else:
        return jsonify({"message": "This action require login"}), status.NOT_FOUND
