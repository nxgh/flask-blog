import json

from flask import request, make_response, redirect, url_for
from flask_restful import Resource
from webargs.flaskparser import parser

from app.extension import mongo
from app.errors import api_abort
from app.email import send_confirm_email
from app.resource.user.models import user
from app.resource.user.auth import (
    generate_token, 
    auth_required, 
    generate_auth_email_token,
    validate_auth_email_token
)
from app.resource.user.forms import (
    signup_args,
    login_args,
)



class User(Resource):

    method_decorators = {
        'put': [auth_required]
    }
    
    def get(self, user_id):
        """
        根据用户id返回用户信息
        根据用户设置返回特定的信息,默认全部返回
        url: '/user/<string:user_id>'
        methods: 'get',
        return: {
            
        }
        """

        result = user.find_one(user_id, flag=False)

        return result

    def post(self):
        """
        用户注册
        url: '/user'
        method: post
        parmas: {
            username: "",
            email:"",
            password:"",
            location:"",
        }
        """
        args = parser.parse(signup_args, request)
        if user.validate_email_exist(args['email']): 
            return api_abort(422, "Eamil已注册")
        elif user.validate_username_exist(args['username']): 
            return api_abort(422, "用户名已存在")

        # 先将user信息存储数据库
        # 发送验证邮件
        # 验证通过则存入
        # 不通过则删除用户
        # 客户端重新登录
        user_info = {
            "username": args['username'],
            "email": args['email'].lower(),
            "password": args['password'],
        }
        user_id = user.insert(user_info)

        confim_token = generate_auth_email_token(user_id)

        config_url = url_for('user_bp.confimtoken',token=confim_token, _external=True)

        send_confirm_email(args['email'], config_url)
        # return redirect(url_for('user.configm_token',token=confim_token))
        return {
            "url": config_url
        }

class ConfimToken(Resource):

    def get(self,token):
        result = validate_auth_email_token(token)
        if result["status"]:
            user_id = result["user_id"]
            user.update(user_id, "auth",True)
        return redirect("http://127.0.0.1:8080/login.html")




class Token(Resource):
    

    def post(self):
        """
        用户登录
        url: '/token'
        method: Post
        params: {
            email: "",
            password: "",
            remember:booleam,
        }
        return {
            user_info
        }
        """
        args = parser.parse(login_args, request)
        email = args['email'].lower()
        password = args['password'] 

        user_id = user.validate_login(email, password)

        if args['remember']:
            token = generate_token(user_id)
        else:
            token = generate_token(user_id, days=0)

        user.update_login_time(user_id)
        

        data =  {
            'token': token,
            'token_type': 'JWT',
            'user_name': user.find_one(user_id, False)['username']
        }
        
        headers = {
            'Cache-Control' :'no-store',
            'Pragma' :'no-cache'
        }
        resp = make_response(json.dumps(data))
        resp.headers.extend(headers or {})
        return resp
    
