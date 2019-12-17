#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask import request, current_app
from flask_restful import Resource
from webargs.flaskparser import parser

from app.api.auth import permission_required
from app.forms.blog import post_args
from app.errors import api_abort
from app.models.blog import Post


"""
定义 /posts 和 /post/<:id>  
"""

class Posts(Resource):

    def get(self):
        '''返回文章集合'''
        # print(post.find_all())
        try:
            data = json.loads(Post.objects.all().only('id', 'title', 'category', 'tags').to_json())
            if not data: raise Exception('post not found')
            for i in data:
                i['id'] = i['_id']['$oid']
                del i['_id']
            current_app.logger.info(data)
            return {
                "posts": data
            }
        except Exception as e:
            current_app.logger.error(e)
            return api_abort(404)

class PostApi(Resource):
    # method_decorators = {
    #     'post': [admin_required],
    #     'put': [admin_required],
    #     'delete': [admin_required],
    # }
    def get(self,post_id):
        '''根据id返回文章内容'''
        try: 
            post = Post.query_post_by_id(id=post_id)
            return post
        except Exception as e:
            current_app.logger.error(e)
            return api_abort(404)

    def post(self):
        '''新建文章'''
        data = parser.parse(post_args, request)
        try:
            p = Post(
                    title = data['title'],
                    content = data['content'],
                    category = data['category'],
                    tags = data['tags'],
                )
            p.save()
        except Exception as e:
            current_app.logger.error(e)
            return api_abort(500)
        return '', 201

    def put(self,post_id):
        '''更新文章 TODO:'''
        data = request.get_json()
        print(data)
        try:
            # data = parser.parse(post_args, request)
            p = Post(id=post_id)
            Post.objects(id=post_id).update_one(set__title=data['title'])
            p.reload()
            return ''
        except Exception as e:
            current_app.logger.error(e)
            return api_abort(500)

    def delete(self,post_id):
        '''删除文章'''
        try:
            p = Post.objects(id=post_id)
            if p is None: return api_abort(404)
            p.delete()
        except Exception as e:
            current_app.logger.errors(e)
            return api_abort(404)
        return '', 204