import json

from flask import request, make_response
from flask_restful import Resource
from webargs.flaskparser import parser

from app.models.user import user
from app.auth.auth import generate_token, auth_required
from app.forms.user import login_args


class Token(Resource):

    method_decorators = {
        "get": [
            auth_required
        ]
    }

    def get(self):
        return {
            "status": True
        }

    def post(self):
        """
        用户登录
        Args:
            email
            pwd
        Return:
            {
                token: 
                token_type:
            }
        """
        args = parser.parse(login_args, request)
        email = args['email'].lower()
        password = args['pwd']
        ip = request.remote_addr

        user_id = user.validate_user_exist(email, password)
        token = generate_token(user_id, days=0, hours=6, seconds=120)

        user.update_login_status(user_id, ip)

        data = {
            'token': token,
            'type': 'Bearer',
        }

        headers = {
            'Cache-Control': 'no-store',
            'Pragma': 'no-cache'
        }
        resp = make_response(json.dumps(data))
        resp.headers.extend(headers or {})
        return resp
