from flask import request, jsonify, Blueprint
from http import HTTPStatus as status
from bson import json_util, ObjectId

from database.db_config import mongo
from flask_jwt_extended import jwt_required

order_routes = Blueprint("order_routes", url_prefix="orders")
db = mongo.get_database("testcart").get_collection("orders")


@order_routes.route("/search", methods=["GET"])
@jwt_required
def get_orders():
    return {}
