import re
from webargs import fields, validate, ValidationError
from flask import current_app


def validateEmail(email):
    pattern = re.compile(r'\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}')
    current_app.logger.info(f'[validateEamil]: { pattern.match(email)}')
    if pattern.match(email) == None:
        raise ValidationError("Email Illegal")

def validatePwd(pwd):
    # 至少 8位, 一个小写字母，一个大写字母，一个数字,一个特殊字符[$@$!_%*?&]
    # pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?_&])[A-Za-z\d$@$!_%*?&]{8,}')
    # current_app.logger.info(f'[validatePwd]: { pattern.match(pwd)}')
    # if pattern.match(pwd) == None:
    #     raise ValidationError("Password Illegal")
    pass    

login_args = {
    "email": fields.Str(required=True,validate=validateEmail, locations="json"),
    "password": fields.Str(required=True,validate=validatePwd, locations="json"),
}

signup_args = {
    "username": fields.Str(required=True,validate=validate.Length(1,48), locations="json"),
    "password": fields.Str(required=True,validate=validatePwd, locations="json"),
    "email": fields.Str(required=True,validate=validateEmail, locations="json"),
}
