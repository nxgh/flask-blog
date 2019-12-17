import json
import os
import random

import requests
from flask import request, make_response, redirect, current_app, g
from flask_restful import Resource
from webargs.flaskparser import parser

from app.errors import api_abort
from app.api.auth import generate_token, permission_required
from app.models.user import User
from app.forms.user import signup_args

# from app.models.user import user

class UserApi(Resource):

    # method_decorators = {
    #     'get': [auth_required]
    # }

    def get(self):
        print(g.user)
        return 'success'

    def post(self):
  
        args = parser.parse(signup_args, request)
        if User.objects(username=args['email']):
            return api_abort(422, "Eamil已注册")
        elif User.objects(username=args['username']):
            return api_abort(422, "用户名已存在")
        try:
            u = User(
                    email = args["email"].lower(),
                    username = args["username"],
                    # TODO: nginx
                    avatar = 'http://192.168.1.106:8000/avatar'
            )
            u.set_password(args["password"])
            u.save()
            return '', 201
        except Exception as e:
            current_app.logger.error(e)
            return api_abort(500)
