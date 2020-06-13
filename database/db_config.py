from flask_pymongo import PyMongo
import urllib
from singleton_decorator import singleton

@singleton
class Database:
  mongo = None
  def init_db(self, app):
    app.config['MONGO_DBNAME'] = 'notice'
    app.config['MONGO_URI'] = 'mongodb+srv://mmstq:' + urllib.parse.quote('@Qwerty123') + '@mmstq-dfntv.mongodb.net/notice?retryWrites=true&w=majority'
    self.mongo = PyMongo(app)
    return self.mongo
