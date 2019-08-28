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

SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

def generate_token(user_id, days=15):
    """
    params: {
        user_id: int
        days: int
    }
    payload {
        'iat': 发行时间
        'exp': 过期时间
        'iss': token 签发者
    }
    """
    try:
        payload = {        
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=days, hours=12, seconds=20),  
            'iss': 'admin',
            'data': {
                'id': user_id,
            }
        }
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        ).decode('ascii')
    except Exception as e:
        raise e

def validate_token(token):
    """
    验证 token
    :param token
    :return {
        status: Boolean
        msg: str
    }
    """
    try: 
       payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        
    except jwt.ExpiredSignature:
        return {
            'status': False,
            'msg': 'ExpiredSignature'
        }
    except (jwt.InvalidTokenError, jwt.DecodeError):
        return {
            'status': False,
            'msg': 'InvalidTokenError'
        }
    return {
            'status': True,
            'payload': payload
        }


def validate_admin_token(token):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        print(payload)
    except jwt.ExpiredSignature:
        return {
            'status': False,
            'msg': 'ExpiredSignature'
        }
    except (jwt.InvalidTokenError, jwt.DecodeError):
        return {
            'status': False,
            'msg': 'InvalidTokenError'
        }
    permission = mongo.db.users.find_one({"_id": ObjectId(payload["data"]["id"])})["permission"]
    if permission != "ADMIN":
        return {
            "status": False,
            'msg': 'InvalidTokenError'
        }
    return {
            'status': True
        }
        


def get_token():
   
    if 'Authorization' in request.headers:
        try:
            token_type, token = request.headers['Authorization'].split(None, 1)
        except ValueError:
            # The Authorization header is either empty or has no token
            token_type = token = None
    else:
        token_type = token = None

    return token_type, token


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_type, token = get_token()

        if request.method != 'OPTIONS':
            if token_type is None or token_type.lower() != 'jwt':
                return api_abort(400, 'The token type must be jwt.')
            if token is None:
                return token_missing()
            result = validate_token(token)
            if not result['status']:
                return api_abort(401, error=result['msg'])
        return f(*args, **kwargs)

    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_type, token = get_token()

        if request.method != 'OPTIONS':
            if token_type is None or token_type.lower() != 'jwt':
                return api_abort(400, 'The token type must be jwt.')
            if token is None:
                return token_missing()
            result = validate_admin_token(token)
            if not result['status']:
                return api_abort(401, error=result['msg'])
        return f(*args, **kwargs)

    return decorated

def get_user_id():
    token_type, token = get_token()
    
    result = validate_token(token)
    user_id = result['payload']["data"]["id"]
    return user_id

def generate_auth_email_token(user_id):
    s = Serializer(current_app.config['SECRET_KEY'])

    data = {'user_id': user_id}
    
    return s.dumps(data)

def validate_auth_email_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])

    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return {
            "status":False,
        }

    return {
        "status":True,
        "user_id":data["user_id"]
    }
