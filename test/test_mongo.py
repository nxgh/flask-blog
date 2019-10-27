import pymongo
from datetime import datetime

client = pymongo.MongoClient(
    'mongodb://blog_dev:password@localhost:27017/blog_dev')

# 数据库
BLOGDEV = client['blog_dev']


# 表/集合
posts = BLOGDEV['Posts']
user = BLOGDEV['Users']
test = BLOGDEV['test']

data = {
    "name": "王花花",
    "age": 18,
    "sex": "男"
}

# user.insert_one(data)
# whh = user.find_one({"name": "王花花"})
# print(whh['age'])
def insert(user_info):
    return test.insert_one({
        "username" : user_info["username"],
        "password_hash" : user_info["password"],
        "email" : user_info["email"],
        "authority" : user_info["authority"],
        "login_info": [
            {
            "ip" : user_info['ip'],
            "login_time" : datetime.timestamp(datetime.now()),
            }
        ],
        "locket" : False,
    }).inserted_id

if __name__ == "__main__":
    user_info = {
        "username": "hello",
        "password": "whatthefuck",
        "email": "test@foxmail.com",
        "authority": "user",
        "ip": "127.1.1.103"
    }
    print(type(insert(user_info)))