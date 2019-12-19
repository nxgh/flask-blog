import os
from functools import wraps
from datetime import datetime, timedelta

from bson import ObjectId
from flask import request, current_app, redirect, g
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.errors import api_abort, invalid_token, token_missing
from app.models.user import User

SECRET_KEY = os.getenv("SECRET_KEY", "dev key")


def generate_token(user_id, t="login"):
    user_id = str(user_id)
    expires_in=3600 * 24 * 30
    if t == 'confirm': expires_in=3600 * 3
    elif t == 'reset': expires_in = 3600
    try:
        data = {"user_id": user_id}
        s = Serializer(SECRET_KEY, expires_in=expires_in)
        token = s.dumps(data).decode('ascii')
        current_app.logger.info(f'user_id: {user_id}\n token:{token}')
        return token
    except Exception as e:
        current_app.logger.error(e)
        return api_abort(500)


def validate_token(token):
    s = Serializer(SECRET_KEY)
    try:
        data = s.loads(token)  # data: {'user_id': 'xxx'}
        current_app.logger.info(data)
    except (SignatureExpired, BadSignature) as e:
        current_app.logger.error(e)
        return False
    g.uid = data['user_id']
    return True



def get_token():
    """获取 token 令牌
    Return：
        token_type: 令牌类型，需要为 Bearer
        token: 令牌内容
    """
    if "Authorization" in request.headers:
        try:
            token_type, token = request.headers["Authorization"].split(None, 1)
        except ValueError as e:
            current_app.logger.info(e)
            token_type = token = None
    else:
        token_type = token = None
    return token_type, token




def permission_required(perm):
    def decorated(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            token_type, token = get_token()

            if request.method != "OPTIONS":
                if token is None:
                    return api_abort(400, 'token missing')
                if token_type is None or token_type.lower() != "bearer":
                    return api_abort(400, "The token type must be bearer.")
                
                result = validate_token(token)

                if not result:
                    return api_abort(401, "admin 错误")
                # g.uid = result.get('msg') 
                u = User.objects(id=g.uid).first().has_permission(perm)
                if not u:
                    return api_abort(401, '莫得权限')

            return f(*args, **kwargs)
        return wrapper
    return decorated