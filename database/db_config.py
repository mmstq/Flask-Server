from gevent import monkey
monkey.patch_all()
from pymongo import MongoClient
import urllib
import atexit

database_uri = (
    "mongodb+srv://mmstq:"
    + urllib.parse.quote("@Qwerty123")
    + "@mmstq-dfntv.mongodb.net/testcart?retryWrites=true&w=majority"
)
mongo = MongoClient(database_uri, socketTimeoutMS=5000)


def onExit():
    print("exit")
    mongo.close()


atexit.register(onExit)
