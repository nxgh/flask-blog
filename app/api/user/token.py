import json

from flask import request, make_response, current_app, g, redirect
from flask_restful import Resource
from webargs.flaskparser import parser

from app.models.user import User, Permission
from app.api.auth import generate_token, permission_required, validate_token
from app.forms.user import login_args
from app.errors import api_abort


class Token(Resource):

    method_decorators = {
        "get": [
            permission_required(Permission.FOLLOW)
        ]
    }

    def get(self):
        return {
            "status": True
        }

    def post(self):

        args = parser.parse(login_args, request)

        email = args['email'].lower()
        password = args['password']
        try:
            u = User.objects(email=email).first()
            if not u:
                return api_abort(401, 'Email not exist')
            current_app.logger.info(f'args: {args}\nuid: {str(u.id)}\nusername: {u.username}')
            if not u.validate_password(password):
                return api_abort(401, 'Password Unauthorized')
            return generate_token(str(u.id))
        except Exception as e:
            current_app.logger.error(e)
            return api_abort(500)


class EmailToken(Resource):

    def get(self, token):
        if not validate_token(token):
            return api_abort(401)
        u = User.objects(id=g.uid).first()
        u.add_permission([Permission.COMMENT, Permission.ASK, Permission.DELETE])
        u.save()
        
        return {
            'confirm_email': True
        }