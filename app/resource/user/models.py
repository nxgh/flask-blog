from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from datetime import datetime

from app.extension import mongo
from app.errors import api_abort


class User(object):     

    @staticmethod
    def set_password(pwd):
        password_hash = generate_password_hash(pwd)
        return password_hash

    @staticmethod
    def validate_password(self, password_hash, password):
        return check_password_hash(password_hash, password)

    def validate_email_exist(self, email):
        user_info = mongo.db.users.find_one({"email": email})
        if user_info :
            return True
        return False
    
    def validate_username_exist(self, username):
        user_info = mongo.db.users.find_one({"username": username})
        if user_info :
            return True
        return False

    def validate_login(self, email, pwd):
        '''验证用户是否存在， 若存在返回user_id'''
        user_info = mongo.db.users.find_one_or_404({"email": email})
        if user is None and not self.validate_password(use['password_hash'], pwd):
            return api_abort(400, 'Either the username or password was invalid.')
        else:
            return str(user_info['_id'])


    def insert(self, user_info):
        mongo.db.users.insert_one({
            "username" : user_info["username"],
            "password_hash" : self.set_password(user_info["password"]),
            "email" : user_info["email"],
            "desc": "",
            "avatar" : "",
            "uid": 0, 
            "topics" : [],
            "photos" : [],
            "permission" : "USER",
            "follower" : [],
            "followed" : [],
            "comments" : [],
            "collect" : [],
            "login_info": [
                {
                "location" : "",
                "login_time" : datetime.timestamp(datetime.utcnow()),
                }
            ],
            "locket" : False,
            "setting": [], # 用户设置
            "auth": False,
        })
        user_id = str(mongo.db.users.find_one({"username": user_info["username"]})["_id"])
        return user_id

    def find_one(self, user_id, flag):
        user_info = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if not user_info : # false
            return api_abort(404)
        user_info["object_id"] = str(user_info["_id"])
        del user_info["_id"]
        del user_info["password_hash"]
        del user_info["permission"]
        del user_info["setting"]
        del user_info["email"]

        if flag:
            return user_info
        del user_info["locket"]
        del user_info["login_info"]

        return user_info

    def update(self, user_id, field, value):
        if field == "password":
            mongo.db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {
                    field: self.set_password(value)
                }}
            )
        else: 
            mongo.db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {
                    field: value
                }}
            )
            
        return self.find_one(user_id, flag=True)

    def update_login_time(self, user_id):
        mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$push": {
                "login_info": {
                    "location" : "",
                    "login_time" : datetime.timestamp(datetime.utcnow()),
                }
            }}
        )
        

user = User()