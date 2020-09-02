# from  apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from waitress import serve
from flask_jwt_extended import JWTManager
import atexit
# from flask_socketio import SocketIO, emit

app = Flask(__name__)
jwt = JWTManager(app)
# socketIO = SocketIO(app, port=8000)

# from function import sockets
from routes.encoder import MongoJSONEncoder, ObjectIdConverter
from routes import user, products, notice


# socketIO.on_namespace(sockets.MyCustomNamespace('/username'))
app.config["JWT_SECRET_KEY"] = "mmstq"
app.config["JWT_ERROR_MESSAGE_KEY"] = "message"
app.json_encoder = MongoJSONEncoder
app.url_map.converters["objectid"] = ObjectIdConverter   

@app.route("/")
def homepage():
    return """<h1>Welcome</h1>"""

# @socketIO.on('username_check')
# def check(username):
#     # db = mongo.get_database('testcart').get_collection("users")
#     # print('my_response', username)
#     #     user = self.db.find_one({'username':username})
#         if None:
#             emit("isUsed", True)
#         else:
#             emit("isUsed", False)


app.register_blueprint(user.user_routes)
app.register_blueprint(notice.notice_route)
app.register_blueprint(products.product_routes)


@app.before_first_request
def init():
    notice.get_db_notice()
    notice.scheduler.start()
    atexit.register(lambda: notice.scheduler.shutdown())


if __name__ == "__main__":
    # app.run(debug=True, host="localhost", port=5000)
    serve(app, host="0.0.0.0", port=8000)
    # socketIO.run(app, port=8000)
