import re
from webargs import fields, validate, ValidationError
from app.extension import mongo

def validateEmail(email):

    if len(email) < 7:
        raise ValidationError("Email Illegal")
    elif re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) == None:
        raise ValidationError("Email Illegal")
    elif not mongo.db.users.find_one({"email":email}):
        raise ValidationError("User does not exist")

def validatePwd(pwd):
    # 至少8个字符，至少1个字母，1个数字和1个特殊字符：  
    if re.match("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$", pwd) == None:
        raise ValidationError("Password Illegal")

signup_args = {
    "username": fields.Str(required=True,validate=validate.Length(1,48), locations="json"),
    "password": fields.Str(required=True,validate=validatePwd, locations="json"),
    "email": fields.Str(required=True,validate=validateEmail, locations="json"),
}

login_args = {
    "email": fields.Str(required=True,validate=validateEmail, locations="json"),
    "password": fields.Str(required=True,validate=validatePwd, locations="json"),
    "remember": fields.Bool(required=True, locations="json")
}

update_args = {
    "email": fields.Str(validate=validateEmail, locations="json"),
    "password": fields.Str(validate=validatePwd, locations="json"),
    "desc": fields.Str(validate=validate.Length(1,128), locations="json"),
}