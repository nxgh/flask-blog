from webargs import fields, validate

post_args = {
    "title": fields.Str(required=True,validate=validate.Length(1,48), locations="json"),
    "body": fields.Str(required=True, locations="json"),
    "category": fields.Str(required=True,validate=validate.Length(1,36), locations="json"),
}

comment_args = {
    "body": fields.Str(required=True, locations="json"),
    "post_id": fields.Str(required=True, validate=validate.Length(1,128),locations="json"),
    "reply_id": fields.Str(required=False, locations="json"),
    "reply_name": fields.Str(required=False, locations="json"),
}