from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS


blog_bp = Blueprint('blog_bp', __name__)
user_bp = Blueprint('user_bp', __name__)

CORS(blog_bp)
CORS(user_bp)

blog_api = Api(blog_bp)
user_api = Api(user_bp)


from app.api.post.category import Categories, Category
from app.api.post.posts import PostApi, Posts
from app.api.post.comments import Comments

from app.api.user.user import UserApi
from app.api.user.oauth import GitToken, GitUser
from app.api.user.token import Token
from app.api.user.avatar import AvatarApi


blog_api.add_resource(Posts, "/posts")
blog_api.add_resource(Categories, "/categories")
blog_api.add_resource(PostApi, "/post", "/post/<string:post_id>")
blog_api.add_resource(Category, "/category", "/category/<string:category>")
blog_api.add_resource(Comments, "/comment", "/comment/<string:comment_id>")

user_api.add_resource(Token, '/token')
user_api.add_resource(UserApi, '/user')

user_api.add_resource(GitToken, '/oauth/github')
user_api.add_resource(GitUser, '/oauth/redirect')

blog_api.add_resource(AvatarApi, "/avatar")


