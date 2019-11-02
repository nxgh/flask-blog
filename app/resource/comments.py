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
            reply_id: None,
            reply_name: None |  
        '''
        username = get_user_info()["username"]
        user_id  = get_user_info()["id"]
       
        args = parser.parse(comment_args, request)

        if not args.get('reply_id') or args['reply_id'] == None:
            comment = {
                "username": username,
                "user_id": user_id,
                "body": args['body'],
            }
            post.add_comment(args["post_id"], comment)
            return 'add_comment Success', 201
        else:
            comment = {
                "username": username,
                "user_id": user_id,
                "body": args['body'],
                "reply_id": args['reply_id'],
                "reply_name": args['reply_name']
            }
            post.add_reply(args['reply_id'], comment)
            return 'add_reply Success', 201

    def delete(self, comment_id):
        '''删除评论'''
        pass