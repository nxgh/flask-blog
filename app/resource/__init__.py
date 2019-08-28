from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS


blog_bp = Blueprint('blog_bp', __name__)
user_bp = Blueprint('user_bp', __name__)

CORS(blog_bp)
CORS(user_bp)

blog_api = Api(blog_bp)
user_api = Api(user_bp)


from app.resource.blog.blog import Post, Posts, Category, Comments, Categories
from app.resource.user.user import User, Token, ConfimToken


blog_api.add_resource(Posts, "/posts")
blog_api.add_resource(Categories, "/categories")
blog_api.add_resource(Post, "/post", "/post/<string:post_id>")
blog_api.add_resource(Category, "/category", "/category/<string:category>")
blog_api.add_resource(Comments, "/comment", "/comment/<string:comment_id>")

user_api.add_resource(User, '/user', '/user/<string:user_id>')
user_api.add_resource(Token, '/token')
user_api.add_resource(ConfimToken, '/confim/<string:token>')


