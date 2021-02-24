from flask import Flask
from flask_jwt_extended import JWTManager
import atexit
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
jwt = JWTManager(app)
socketIO = SocketIO(app, async_mode="gevent")
CORS(app=app)

from function import sockets

from routes.encoder import MongoJSONEncoder, ObjectIdConverter
from routes import user, products, notice


socketIO.on_namespace(sockets.MyCustomNamespace('/username'))
app.config["JWT_SECRET_KEY"] = "mmstq"
app.config["JWT_ERROR_MESSAGE_KEY"] = "message"
app.json_encoder = MongoJSONEncoder
app.url_map.converters["objectid"] = ObjectIdConverter   

@app.route("/")
def homepage():
    return """<h1>Welcome</h1>"""


app.register_blueprint(user.user_routes)
app.register_blueprint(notice.notice_route)
app.register_blueprint(products.product_routes)


@app.before_first_request
def init():
    notice.get_db_notice()
    notice.scheduler.start()
    atexit.register(lambda: notice.scheduler.shutdown())

if __name__ == "__main__":
    app.run()
    
