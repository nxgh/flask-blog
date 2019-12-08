import json
import os

import requests
from flask import request, make_response, redirect, current_app, g
from flask_restful import Resource
from webargs.flaskparser import parser

from app.errors import api_abort
from app.models.user import user
from app.api.auth import generate_token, admin_required, auth_required
from app.forms.user import signup_args


class User(Resource):

    method_decorators = {
        'get': [auth_required]
    }

    def get(self):
        print(g.user)
        return 'success'

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

        if user.validate_user_exist({'email': args["email"]}):
            return api_abort(422, "Eamil已注册")
        elif user.validate_user_exist({'username': args["username"]}):
            return api_abort(422, "用户名已存在")

        user_info = {
            "username": args["username"],
            "email": args["email"].lower(),
            "password": args["password"],

        }
        user_id = user.insert(user_info)

        data = {
            "token": generate_token(user_id),
            "type": "Bearer",
        }
        headers = {
            "Cache-Control": "no-store",
            "Pragma": "no-cache"
        }
        resp = make_response(json.dumps(data))
        resp.headers.extend(headers or {})
        return resp
