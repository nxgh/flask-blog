from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS


blog_bp = Blueprint('blog_bp', __name__)
user_bp = Blueprint('user_bp', __name__)

CORS(blog_bp)
CORS(user_bp)

blog_api = Api(blog_bp)
user_api = Api(user_bp)


from app.resource.category import Categories, Category
from app.resource.posts import Post, Posts
from app.resource.comments import Comments
from app.resource.user import User
from app.resource.token import Token


blog_api.add_resource(Posts, "/posts")
blog_api.add_resource(Categories, "/categories")
blog_api.add_resource(Post, "/post", "/post/<string:post_id>")
blog_api.add_resource(Category, "/category", "/category/<string:category>")
blog_api.add_resource(Comments, "/comment", "/comment/<string:comment_id>")

user_api.add_resource(Token, '/token')
user_api.add_resource(User, '/users')


