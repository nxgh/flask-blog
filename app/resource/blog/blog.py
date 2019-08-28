from flask import request
from flask_restful import Resource
from webargs.flaskparser import parser
from bson import ObjectId

from app.resource import blog_bp
from app.resource.user.auth import auth_required, admin_required, get_user_id
from app.resource.blog.forms import post_args, comment_args
from app.resource.blog.models import post

from app.extension import mongo


# class Index(Resource):

#     def get(self):
#         '''返回url列表
#         
#         '''
#         return {
#         
#         }


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
    
class Comments(Resource):
    
    method_decorators = {
        'post': [auth_required],
        'delete': [admin_required]
    }
    def post(self):
        '''提交评论'''
        user_id = get_user_id()
        username = mongo.db.users.find_one({"_id": ObjectId(user_id)})["username"]
        args = parser.parse(comment_args, request)
        post_id = args["post_id"]
        comment = {
            "username": username,
            "body": args['body']
        }
        post.add_comment(post_id, comment)
        return '', 201

    def delete(self, comment_id):
        '''提交评论'''
        pass

class Category(Resource):

    def get(self, category):
        '''返回某分类下所有文章'''
        
        
        posts = []
        post_info = mongo.db.posts.find({"category": category})
        for post in post_info:
            post["id"] = str(post["_id"])
            del post["_id"]
            posts.append(post)
        return{
            "posts":posts
        }
class Categories(Resource):

    def get(self):
        '''返回某分类下所有文章'''
        
        
        categories = set()
        post_info = mongo.db.posts.find({}, {'category':1,'_id':0})
        for cate in post_info:
            categories.add(cate['category'])
        
        return {
            'categories': list(categories)
        }
    