from faker import Faker
import pymongo
import random
import time
from datetime import datetime
from bson import ObjectId, timestamp


fake = Faker('zh-CN')
client = pymongo.MongoClient('mongodb://blog_dev:password@localhost:27017/blog_dev')

BLOGDEV = client['blog_dev']
posts = BLOGDEV['posts']


post_id = "5db17bd82b0e1ab186c96eec"


def add_comment(self, post_id, comment):
    posts.update(
        {"_id": ObjectId(post_id)},
        {
            "$push": {
                "comments": {
                    "id": ObjectId(),
                    "username": comment["username"],
                    "body": comment["body"],
                    "reply": []
                }
            }
        }
    )

def reply_comment(self, reply_id, comment):

    posts.update(
        {"comments.id": ObjectId(reply_id)},
        {
            "$push": {
                "id": ObjectId(),
                "username": comment["username"],
                "body": comment["body"],
                "reply_id": ""
            }
        }
    )


if __name__ == "__main__":
    comment = {
        "username": "李密",
        "body": "唐室的江山为兄掌，封你个一字并肩王",
    }
    reply1 = {
        "usernmae": "王伯当",
        "body": "说什么一字并肩王，羞得王勇面无光",
    }
    reply2 = {
        "username": "李密",
        "body": "君臣义路好商量，李密打马朝前闯",
    }
    reply3 = {
        "usernmae": "王伯当",
        "body": "王伯当错保无义的王",
    }



