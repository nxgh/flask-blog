import json

from bson import ObjectId
from mongoengine import (
    StringField, 
    ReferenceField, 
    EmbeddedDocument, 
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    Document,
    ListField,
    CASCADE, DENY, NULLIFY,
    IntField,
    BooleanField,
    ObjectIdField,
    queryset_manager
)
# from mongoengine.queryset.manager import queryset_manager

from flask import current_app
from app.errors import api_abort
from .user import User




class Comment(EmbeddedDocument):
    cid = ObjectIdField(default=lambda: ObjectId())
    author = ReferenceField(User)
    content = StringField()
    reply = ObjectIdField()




class Post(Document):
    # reverse_delete_rule=CASCADE 级联删除
    # author = ReferenceField(User, reverse_delete_rule=NULLIFY)

    title = StringField(max_length=1024, required=True)
    content = StringField()
    like = IntField(default=0)
    can_comment = BooleanField(default=True)

    category = StringField(max_length=30)
    tags = ListField(StringField(max_length=30))
    comments = EmbeddedDocumentListField('Comment')

    @classmethod
    def query_post_by_id(cls, id):
        # FIXME: 写法好丑
        try:
            post = cls.objects(id=id).first()
            if post is None: raise Exception('post not found')
            comments = []
            for i in post.comments:
                comment = {
                    'author_id': i.author.id,
                    'username': i.author.username,
                    'avatar': i.author.avatar,
                    'content': i.content,
                    "comment_id": i.cid
                }
                comments.append(comment)
            print(comments)

            post.comments = comments
            data = json.loads(post.to_json(use_db_field=False))

            data['id'] = data['id']['$oid']
            del data['_id']
            for j in data['comments']:
                j['author_id'] = j['author_id']['$oid']
            return data

        except Exception as e:
            current_app.logger.error(e)
            return False

