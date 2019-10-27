from flask import request
from flask_restful import Resource
from webargs.flaskparser import parser
from bson import ObjectId

from app.auth.auth import auth_required, get_user_info, admin_required
from app.forms.blog import comment_args
from app.models.blog import post

from app.extension import mongo


class Comments(Resource):
    
    method_decorators = {
        'post': [auth_required],
        'delete': [admin_required]
    }

    def post(self):
        '''提交评论
        Args:
            body: 
            post_id: 5db17a4f14fc6a9a236c8d63
            replay_id: None or  
        '''
        username = get_user_info()["username"]
        args = parser.parse(comment_args, request)
        post_id = args["post_id"]
        comment = {
            "username": username,
            "body": args['body'],
            "replay_id": args['replay_id'] or None
        }
        post.add_comment(post_id, comment)
        return '', 201

    def delete(self, comment_id):
        '''删除评论'''
        pass