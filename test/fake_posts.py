from faker import Faker
import pymongo
import random
import time
from datetime import datetime
from bson import ObjectId, timestamp

post = """

"""
fake = Faker('zh-CN')
client = pymongo.MongoClient(
    'mongodb://blog_dev:password@localhost:27017/blog_dev')

BLOGDEV = client['blog_dev']
posts = BLOGDEV['posts']


comment_id = "5dbc09faf4fb46d0f0f7a538"
comment = {
    "body": "管理员回复!",
	"post_id": "5db7e64432841e5c643ab2c3",
	"reply_name": "Test1",
	"reply_id": "5dbae0183af1d43457bfe89a",
    "username": "test",
    "user_id": "test",
}

if __name__ == "__main__":
    posts.update(
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