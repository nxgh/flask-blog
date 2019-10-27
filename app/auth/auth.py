import os, time
from functools import wraps
from datetime import datetime, timedelta

from bson import ObjectId
import jwt
from flask import request, current_app, redirect, flash
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


from app.errors import api_abort, invalid_token, token_missing
from app.extension import mongo

SECRET_KEY = os.getenv("SECRET_KEY", "dev key")


def generate_token(user_id, days=15, hours=0, seconds=120):
    """
    Args:
        user_id: int
    Return:
        以ascii格式，返回编码后的token令牌
        eg: 
    """
    try:
        payload = {
            "iat": datetime.utcnow(), # 发行时间
            "exp": datetime.utcnow() + timedelta(days=days, hours=hours, seconds=seconds), # 过期时间
            "iss": "nxgh", # 签发者
            "data": {
                "id": user_id,
                "authority": mongo.db.users.find_one({"_id": ObjectId(user_id)})["authority"]
            }
        }
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm="HS256"
        ).decode("ascii")
    except Exception as e:
        raise e

def validate_token(token):
    """验证用户 token 令牌

    Args:
        token: String

    Return: 
        {
            status: Boolean, token是否合法
            msg: String， 正确/错误信息
            permission: String, 用户角色
        }

    """
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
    except jwt.ExpiredSignature:
        return {
            "status": False,
            "msg": "ExpiredSignature"
        }
    except (jwt.InvalidTokenError, jwt.DecodeError):
        return {
            "status": False,
            "msg": "InvalidTokenError"
        }
    permission = mongo.db.users.find_one({"_id": ObjectId(payload["data"]["id"])})["authority"]
    return {
            "status": True,
            "payload": payload,
            "permission": permission
        }


def get_token():
    """获取 token 令牌
    Return：
        token_type: 令牌类型，需要为 Bearer
        token: 令牌内容
    """

    if "Authorization" in request.headers:
        try:
            token_type, token = request.headers["Authorization"].split(None, 1)
        except ValueError:
            # The Authorization header is either empty or has no token
            token_type = token = None
    else:
        token_type = token = None

    return token_type, token


def auth_required(f):
    """ 普通用户验证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token_type, token = get_token()

        if request.method != "OPTIONS":
            if token_type is None or token_type.lower() != "bearer":
                return api_abort(400, "The token type must be bearer.")
            if token is None:
                return token_missing()
            result = validate_token(token)
            print(result)
            if not result["status"]:
                return api_abort(401, "auth 错误")
        return f(*args, **kwargs)

    return decorated

def admin_required(f):
    """ 管理员验证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token_type, token = get_token()

        if request.method != "OPTIONS":
            if token_type is None or token_type.lower() != "bearer":
                return api_abort(400, "The token type must be bearer.")
            if token is None:
                return token_missing()
            result = validate_token(token)
            if not result["status"] or result["permission"] != "admin":
                return api_abort(401, "admin 错误")
        return f(*args, **kwargs)

    return decorated

def get_user_info():
    """ 根据token信息获取用户信息

    Return: 

      返回用户信息，示例：

        {
            "id": "5d9ae058cd534a0e8fc212f6"
            "username": "王花花"
            "email": "whh@foxmail.com"
            "authority": "USER"
            "login_info": [
                {"ip": "192.168.1.106", "login_time": 1570402264.213736}
            ]
            "locket": False
        }

    """
    token_type, token = get_token()

    result = validate_token(token)
    user_id = result["payload"]["data"]["id"]
    userinfo = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    del userinfo["_id"]
    del userinfo["password_hash"]
    userinfo["id"] = user_id
    return userinfo
