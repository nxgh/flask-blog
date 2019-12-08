import os
from functools import wraps
from datetime import datetime, timedelta

from bson import ObjectId
from flask import request, current_app, redirect, flash, g
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.models.user import user
from app.errors import api_abort, invalid_token, token_missing
from app.extension import mongo

SECRET_KEY = os.getenv("SECRET_KEY", "dev key")


def generate_token(user_id):
    """
    Args:
        user_id: int
    Return:
        以ascii格式，返回编码后的token令牌
    """
    if type(user_id) != str:
        user_id = str(user_id)
    current_app.logger.info(user_id)
    data = {"user_id": user_id}
    s = Serializer(SECRET_KEY, expires_in=3600 * 24 * 30)
    token = s.dumps(data).decode('ascii')

    return token


def validate_token(token):
    """验证用户 token 令牌
    Args:
        token: String

    Return: 
        {
            status: bool, token是否合法
            res: 一个错误消息 或是 user_id
        }

    """
    s = Serializer(SECRET_KEY)
    try:
        # print(token)
        data = s.loads(token)  # data: {'user_id': 'xxx'}
        current_app.logger.info(data)
    except (SignatureExpired, BadSignature):
        return {
            "status": False,
            "res": "Bad Token Or Token Expired"
        }
    return {
        "status": True,
        'res': data['user_id']
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
            token_type = token = None
    else:
        token_type = token = None
    return token_type, token


def auth_required(f):
    """ 普通用户验证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token_type, token = get_token()
        # current_app.logger.info(token)
        if request.method != "OPTIONS":
            if token is None:
                return token_missing()
            if token_type is None or token_type.lower() != "bearer":
                return api_abort(400, "The token must be exist and type must be bearer.")
    
            result = validate_token(token)
            current_app.logger.info(f'auth_required validate_token {result}')
            if not result["status"]:
                return api_abort(401, "Not Auth")
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
            role = user.find(result).get('role', '')
            current_app.logger.info(f'auth_required validate_token {result}')
            if not result["status"] and role != 'ADMIN':
                return api_abort(401, "Not Admin")
        return f(*args, **kwargs)

    return decorated
