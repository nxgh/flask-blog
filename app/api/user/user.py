import json
import os
import random

import requests
from flask import request, make_response, redirect, current_app, g
from flask_restful import Resource
from webargs.flaskparser import parser

from app.errors import api_abort
from app.api.auth import generate_token, permission_required, get_token, validate_token
from app.models.user import User, Permission
from app.forms.user import signup_args
from app.email import send_confirm_email

class UserApi(Resource):


    def get(self, user_id):

        token_type, token = get_token()
        u = User.objects(id=user_id).first()
        if not u: return api_abort(404)
        user_info = {
            'id': str(u.id),
            'username': u.username,
            'avatar': u.avatar,
            'followed': u.followed,
            'follower': u.follower,
            'question': u.question,
        }
        if token != None and validate_token(token) and g.uid == user_id:
            user_info['emali'] = u.email
            return user_info
        else:
            return user_info


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
                    avatar = 'http://192.168.1.106:8000/avatar/r{0}.png'.format(random.randint(1, 10))
            )
            u.set_password(args["password"])
            u.save()
            if os.getenv('FLASK_ENV') == 'development':
                # 发送 email
                uid = User.objects(email=args['email']).first().id
                send_confirm_email(
                    args['email'],
                    args['username'],
                    generate_token(uid))
            return '', 201
        except Exception as e:
            current_app.logger.error(e)
            return api_abort(500)
