
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

from werkzeug.security import generate_password_hash, check_password_hash

class Permission:
    FOLLOW = 1
    COLLECT = 2
    COMMENT = 4
    ASK = 8
    DELETE = 16
    MODERATE = 32
    ADMIN = 64

role_map = {
    'Visitor': [Permission.FOLLOW, Permission.COLLECT], # 3
    # 31
    'User': [
        Permission.FOLLOW, Permission.COLLECT, 
        Permission.COMMENT, Permission.ASK, Permission.DELETE],
    # 63
    'Moderator': [
        Permission.FOLLOW, Permission.COLLECT, Permission.COMMENT, 
        Permission.ASK, Permission.DELETE, Permission.MODERATE],
    # 127 
    'Administrator': [
        Permission.FOLLOW, Permission.COLLECT, Permission.COMMENT, 
        Permission.ASK, Permission.DELETE, Permission.MODERATE, Permission.ADMIN]
}


class User(Document):
    username = StringField(max_length=50)
    email = StringField(unique=True)
    password_hash = StringField(max_length=128)
    avatar = StringField()

    followed = ListField(ReferenceField('self', reverse_delete_rule=CASCADE))
    follower = ListField(ReferenceField('self', reverse_delete_rule=CASCADE))
    role = IntField(default=sum(role_map['Visitor']))
    question = ListField(ReferenceField('Question'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_permission(self, perm):
        self.role += perm

    def remove_permission(self, perm):
        self.role -= perm
    
    def reset_permission(self, perm):
        self.role = 0

    def has_permission(self, perm):
        return self.role & perm == perm
    







