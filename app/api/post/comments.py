from flask import request, g, current_app
from flask_restful import Resource
from webargs.flaskparser import parser
from bson import ObjectId

from app.errors import api_abort
from app.api.auth import permission_required
from app.models.user import Permission, User
from app.models.blog import Post, Comment
from app.forms.blog import comment_args, delete_comment_args


class Comments(Resource):
    
    method_decorators = {
        'post': [permission_required(Permission.COMMENT)],
        'delete': [permission_required(Permission.DELETE)],
    }

    def post(self):
        '''提交评论
        Args:
            content: 
            post_id: 5db17a4f14fc6a9a236c8d63
            reply_id: 5db17a4f14fc6a9a236c8d63 or None
        ''' 
        args = parser.parse(comment_args, request)
        author = User.objects(id=g.uid).first()
        post = Post.objects(id=args['post_id']).first()

        if not post: return api_abort(404)
        try:
            c = Comment(
                author = author,
                content = args['content'],
                reply = args.get('reply_id', '') or args['post_id']
            )
            post.comments.append(c)
            post.save()
            return '', 201
        except Exception as e:
            current_app.logger.error(e)
            return api_abort(500)
      
    def delete(self, comment_id):
        '''删除评论'''

        # step1. 根据 cid 查询评论作者的 id
        # step2. 判断 g.uid 是否等于作者 id
        # step2.1. 等于则执行删除操作
        # step2.2. 否则返回 422
        # author = User.objects(id=g.uid).first()

        args = parser.parse(delete_comment_args, request)
        post_id = args['post_id']

        try:
            comment_author_id = Post.objects.get(id=post_id).comments.filter(cid=comment_id).first().author.id
        except Exception as e:
            current_app.logger.error(e)
            return api_abort(404)
        current_app.logger.info(f'{comment_author_id}, {g.uid}')
        if str(comment_author_id) == g.uid:
            Post.objects(id=post_id).update_one(pull__comments__cid=comment_id)
            return '', 204
        else:
            return api_abort(403)
