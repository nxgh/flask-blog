from flask_restful import Resource
from flask import send_file

from app.email import send_confirm_email
from ..auth import generate_token


class AvatarApi(Resource):

    def get(self, file_name):
        return send_file('avatars/' + file_name)
