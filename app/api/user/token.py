import json

from flask import request, make_response, current_app, g
from flask_restful import Resource
from webargs.flaskparser import parser

from app.models.user import user
from app.api.auth import generate_token, auth_required
from app.forms.user import login_args
from app.errors import api_abort


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
        password = args['password']

        user_info = user.find({'email': email})

        if not user_info:
            return api_abort(400, 'Email not exist')

        current_app.logger.info(f'login_args: {args},\n user_info:  {user_info}')

        
        if user.validate_password(user_info.get('password_hash', ''), password):
            data = {
                'token': generate_token(user_info.get('_id')),
                'type': 'Bearer',
            }
            headers = {
                'Cache-Control': 'no-store',
                'Pragma': 'no-cache'
            }
            resp = make_response(json.dumps(data))
            resp.headers.extend(headers or {})
            return resp
        else:
            return api_abort(400, "Password was invalid.")
