import re
from webargs import fields, validate, ValidationError
from app.extension import mongo

def validateEmail(email):

    if len(email) < 7:
        raise ValidationError("Email Illegal")
    elif re.match("[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?", email) == None:
        raise ValidationError("Email Illegal")
    elif not mongo.db.users.find_one({"email":email}):
        raise ValidationError("User does not exist")

def validatePwd(pwd):
    # 至少8个字符，至少1个字母，1个数字和1个特殊字符：  
    if re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[\s\S]{8,16}$", pwd) == None:
        raise ValidationError("Password Illegal")

# login_args = {
#     "email": fields.Str(required=True,validate=validateEmail, locations="json"),
#     "password": fields.Str(required=True,validate=validatePwd, locations="json"),
# }

# signup_args = {
#     "username": fields.Str(required=True,validate=validate.Length(1,48), locations="json"),
#     "pwd": fields.Str(required=True,validate=validatePwd, locations="json"),
#     "email": fields.Str(required=True,validate=validateEmail, locations="json"),
# }
login_args = {
    "email": fields.Str(required=True, locations="json"),
    "pwd": fields.Str(required=True, locations="json"),
}

signup_args = {
    "username": fields.Str(required=True, locations="json"),
    "pwd": fields.Str(required=True, locations="json"),
    "email": fields.Str(required=True, locations="json"),
}
