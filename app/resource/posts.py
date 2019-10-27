from flask import request
from flask_restful import Resource
from webargs.flaskparser import parser

from app.auth.auth import admin_required
from app.forms.blog import post_args
from app.models.blog import post


class Posts(Resource):

    def get(self):
        '''返回文章集合'''
        return {
            "posts":post.find_all()
        }

class Post(Resource):
    method_decorators = {
        'post': [admin_required],
        'put': [admin_required],
        'delete': [admin_required],
    }
    def get(self,post_id):
        '''根据id返回文章内容'''
        return post.find_one(post_id)

    def post(self):
        '''新建文章'''
        data = parser.parse(post_args, request)
        post.insert(data)
        return '', 201

    def put(self,post_id):
        '''更新文章'''
        data = parser.parse(post_args, request)
        post.update(post_id, data)
        return ''

    def delete(self,post_id):
        '''删除文章'''
        post.delete(post_id)
        return '', 204
    