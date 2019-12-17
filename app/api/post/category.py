from flask_restful import Resource
from app.models.blog import Post

class Category(Resource):

    def get(self, category):
        '''返回某分类下所有文章'''
        
        # posts = []
        # post_info = mongo.db.posts.find({"category": category})
        # for post in post_info:
        #     post["id"] = str(post["_id"])
        #     del post["_id"]
        #     del post["comments"]
        #     posts.append(post)
        # return{
        #     "posts":posts
        # }

class Categories(Resource):
    
    def get(self):
        return {
            'categories': list({i.category for i in Post.objects.all()})
        }

