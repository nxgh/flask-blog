#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, current_app
from flask_restful import Resource
from webargs.flaskparser import parser

from app.api.auth import admin_required
from app.forms.blog import post_args
from app.models.blog import post


"""
定义 /posts 和 /post/<:id>  
"""

class Posts(Resource):

    def get(self):
        '''返回文章集合'''
        # print(post.find_all())
        current_app.logger.info(post.find_all())
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
    