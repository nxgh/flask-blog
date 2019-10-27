import json

from flask import request, make_response
from flask_restful import Resource
from webargs.flaskparser import parser

from app.errors import api_abort
from app.models.user import user
from app.auth.auth import generate_token
from app.forms.user import signup_args


class User(Resource):

    def post(self):
        """用户注册
        Args:
            username
            email
            password
        Return:
            {
                "token": token,
                "token_type": "JWT"
                "authority: 
            }
        """
        args = parser.parse(signup_args, request)
        if user.validate_email_exist(args["email"]):
            return api_abort(422, "Eamil已注册")
        elif user.validate_username_exist(args["username"]):
            return api_abort(422, "用户名已存在")
        ip = request.remote_addr

        user_info = {
            "username": args["username"],
            "email": args["email"].lower(),
            "password": args["pwd"],
            "ip": ip,
            "authority": "user"
        }
        user_id = user.insert(user_info)
        token = generate_token(str(user_id))

        data = {
            "token": token,
            "type": "Bearer",
        }
        headers = {
            "Cache-Control": "no-store",
            "Pragma": "no-cache"
        }
        resp = make_response(json.dumps(data))
        resp.headers.extend(headers or {})
        return resp

        
