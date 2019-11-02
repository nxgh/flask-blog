from flask_restful import Resource
from flask import send_file



class AvatarApi(Resource):

    def get(self, user_id):
        return send_file('avatars/' + str(user_id))