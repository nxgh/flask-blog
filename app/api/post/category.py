from flask_restful import Resource

from app.models.blog import post
from app.extension import mongo

class Category(Resource):

    def get(self, category):
        '''返回某分类下所有文章'''
        posts = []
        post_info = mongo.db.posts.find({"category": category})
        for post in post_info:
            post["id"] = str(post["_id"])
            del post["_id"]
            del post["comments"]
            posts.append(post)
        return{
            "posts":posts
        }

class Categories(Resource):
    
    def get(self):
        '''返回所有文章的分类列表
        Return:
            {
                "categories": [
                    
                ] 
            }
        '''
                
        categories = set()
        post_info = mongo.db.posts.find({}, {'category':1,'_id':0})
        for cate in post_info:
            
            categories.add(cate['category'])
        
        return {
            'categories': list(categories)
        }
    