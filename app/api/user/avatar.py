from flask_restful import Resource
from flask import send_file



class AvatarApi(Resource):

    def get(self):
        return send_file('avatars/anonymous.png')