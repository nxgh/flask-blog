import os

from bson import ObjectId

from app.extension import mongo

author = os.getenv("app_AUTHOR", "nxgh")

class Post(object):

    def insert(self, post):
        mongo.db.posts.insert_one({
            "title": post["title"],
            "body": post["body"],
            "category": post["category"],
            "author": author,
            "comments": [], # {username: "", body:""}
            "type_comment": post["type_comment"],
         
        })
    
    def find_all(self):
        posts = []
        post_info = mongo.db.posts.find({})
        for post in post_info:
            post["id"] = str(post["_id"])
            del post["_id"]
            posts.append(post)
        return posts
    
    def find_one(self, post_id):
        post_info = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
        post_info["id"] = str(post_info["_id"])
        del post_info["_id"]
        return post_info

    def delete(self, post_id):
        mongo.db.posts.delete_one({"_id": ObjectId(post_id)})
        
        return '', 204

    def category_post(self, category):
        posts = []
        post_info = mongo.db.posts.find({"category": category})
        for post in post_info:
            post["id"] = str(post["_id"])
            del post["_id"]
            posts.append(post)
        return posts

    def update(self, post_id, post_info):
        mongo.db.posts.update(
            {"_id": ObjectId(post_id)},
            {
                "$set": {
                    "title": post_info["title"],
                    "body": post_info["body"],
                    "category": post_info["category"],
                    "type_comment": post_info["type_comment"],
                }
            }
        )

    def add_comment(self, post_id, comment):
        mongo.db.posts.update(
            {"_id": ObjectId(post_id)},
            {
                "$push": {
                    "comment": comment
                }
            }
        )

post = Post()