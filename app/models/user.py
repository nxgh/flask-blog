import os
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
        if mongo.db.users.find_one({"username": username}) :
            return True
        return False

    def validate_user_exist(self, email, pwd):
        """验证用户是否存在， 若存在返回user_id"""
        user_info = mongo.db.users.find_one_or_404({"email": email})
        if user is None and not self.validate_password(user["password_hash"], pwd):
            return api_abort(400, "Either the username or password was invalid.")
        else:
            return str(user_info["_id"])


    def insert(self, user_info):
        """
        Args: 

            {
                "username": "王花花"，
                "email": "whh@foxmail.com",
                "password": "Password_123",
                "ip": "127.0.0.1"
            }
        Return: 
        
          <class bson.objectid.ObjectId>
        """
        return mongo.db.users.insert_one({
            "username" : user_info["username"],
            "password_hash" : self.set_password(user_info["password"]),
            "email" : user_info["email"],
            "authority" : user_info["authority"],
            "login_info": [
                {
                "ip" : user_info["ip"],
                "login_time" : datetime.timestamp(datetime.now()),
                }
            ],
            "locket" : False,
        }).inserted_id
        

    def update_login_status(self, user_id, ip):
        mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$push": {
                "login_info": {
                    "ip" : ip,
                    "login_time" : datetime.timestamp(datetime.utcnow()),
                }
            }}
        )

    def get_user_permission(self, user_id):
        return mongo.db.users.find_one({"_id": ObjectId(user_id)})["authority"]
        

user = User()