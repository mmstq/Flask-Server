from flask import request, jsonify, Blueprint
from http import HTTPStatus as status
from database.db_config import mongo
from bson import json_util, ObjectId
import json
from routes.encoder import MongoJSONEncoder, ObjectIdConverter


db = mongo.get_database("testcart").get_collection("products")
product_routes = Blueprint("product_routes", __name__, url_prefix="/products")

@product_routes.route("/search", methods=["GET", "POST"])
def getProduct():
    a = json.loads(request.get_data())

    print(a["Value"])

    queryString = a["Query"]
    queryValue = a["Value"]
    products = db.find({queryString: {"$in": queryValue}})
    return {"items": json.loads(json_util.dumps(products))}


@product_routes.route("/all", methods=["GET", "POST"])
def searchProduct():

    products = db.find({})
    return {"items": json.loads(json_util.dumps(products))}

@product_routes.route("/category", methods=["POST"])
def get_product_by_category():
    data = json.loads(request.get_data())
    
    query = data["Query"]
    value = data["Value"]
    products = db.find({query: {"$in": value}})

    print(products.count())
    return {"items": json.loads(json_util.dumps(products))}
