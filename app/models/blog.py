from bson import ObjectId

from app.extension import mongo


class Post(object):

    def insert(self, post):
        return mongo.db.posts.insert_one({
            "title": post["title"],
            "body": post["body"],
            "category": post["category"],
            "comments": [], # {username: "", body:""}  
        }).inserted_id
    
    def find_all(self):
        posts = []
        post_info = mongo.db.posts.find({})
        for post in post_info:
            post["id"] = str(post["_id"])
            del post["_id"]
            del post["comments"]
            del post["body"]
            posts.append(post)
        return posts
    
    def find_one(self, post_id):
        post_info = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
        post_info["id"] = str(post_info["_id"])
        del post_info["_id"]
        for comment in post_info["comments"]:
            comment["id"] = str(comment["id"])
            for reply in comment["reply"]:
                reply['id'] = str(reply['id'])
        return post_info

    def delete(self, post_id):
        mongo.db.posts.delete_one({"_id": ObjectId(post_id)})
        
        return "", 204

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
                    "comments": {
                        "id": ObjectId(),
                        "username": comment["username"],
                        "user_id": comment["user_id"],
                        "body": comment["body"],
                        "reply": [],
                        "like": 0,
                    }
                }
            }
        )

    def add_reply(self, comment_id, comment):
        mongo.db. posts.update(
            {"comments.id": ObjectId(comment_id)},
            {
                "$push": {
                    "comments.$.reply": {
                        "id": ObjectId(),
                        "username": comment["username"],
                        "user_id": comment["user_id"],
                        "body": comment["body"],
                        "reply_id": comment["reply_id"],
                        "reply_name": comment["reply_name"],
                        "like": 0,
                    }
                }
            }
        )

post = Post()