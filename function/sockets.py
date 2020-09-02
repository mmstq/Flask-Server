# from flask_socketio import Namespace, emit
# from database.db_config import mongo

# class MyCustomNamespace(Namespace):
    
#     def __init__(self, namespace=None):
#         self.db = mongo.get_database('testcart').get_collection("users")
#         super().__init__(namespace=namespace)
#     def on_connect(self):
#         pass

#     def on_disconnect(self):
#         pass

#     def on_username_check(self, username):
#         print('my_response', username)
#         user = self.db.find_one({'username':username})
#         if user:
#             emit("isUsed", True)
#         else:
#             emit("isUsed", False)
        