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
)
from bson import ObjectId

from .user import User


class Answer(EmbeddedDocument):
    _id = ObjectIdField(default=lambda: ObjectId())
    author = ReferenceField('User')
    content = StringField()
    like = IntField(default=0)
    reply = ObjectIdField()

class Question(Document):
    title = StringField(max_length=1024, required=True)
    description = StringField()
    author = ReferenceField('User', reverse_delete_rule=NULLIFY)
    tags = ListField()
    # answer = EmbeddedDocumentListField('Answer')
    answer = EmbeddedDocumentListField('Answer')