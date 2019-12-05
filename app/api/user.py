import json
import os

import requests
from flask import request, make_response, redirect, current_app, g
from flask_restful import Resource
from webargs.flaskparser import parser

from app.errors import api_abort
from app.models.user import user
from app.auth import generate_token, admin_required, auth_required
from app.forms.user import signup_args


class GitToken(Resource):

    def get(self):
        '''返回用户跳转到 Github 的 Url
        URL 指向 GitHub 的 OAuth 授权网址
        '''
        return 'https://github.com/login/oauth/authorize? \
            client_id={0} \
            &scoped=user:email \
            &redirect_uri={1}'.format(os.getenv('GITHUB_CLIENT_ID'), os.getenv('GITHUB_REDIRECT_URL'))


class GitUser(Resource):

    @staticmethod
    def get_access_token(code):

        url = 'https://github.com/login/oauth/access_token? \
            client_id={0} \
            &client_secret={1} \
            &code={2}'.format(os.getenv('GITHUB_CLIENT_ID'), os.getenv('GITHUB_CLIENT_SECRET'), code)
        headers = {'accept': 'application/json'}
        r = requests.post(url, headers=headers).json()
        '''r   
            Success:
              {'access_token': '374171064616b9c53adb9149c356954ec3bf4199', 'token_type': 'bearer', 'scope': ''}
            Exception:
              {'error': 'bad_verification_code', 'error_description': 'The code passed is incorrect or expired.', 'error_uri': 'https://developer.github.com/apps/managing-oauth-apps/troubleshooting-oauth-app-access-token-request-errors/#bad-verification-code'}
        '''
        current_app.logger.info('请求github access_token: {0}'.format(r))

        if r.get('access_token', None):
            return r['access_token']
        else:
            return ''

    @staticmethod
    def get_user_info(access_token):
        user_info = requests.get(
            'https://api.github.com/user',
            headers={
                'accept': 'application/json',
                'Authorization': 'token ' + access_token
            }
        ).json()
        current_app.logger.info('requests github user_info: {0}'.format(user_info))
        return user_info

    def get(self):
        code = request.args.get('code', '')
        if code:
            access_token = self.get_access_token(code)  # token:  '374171064616b...'
            if access_token:

                git_user_info = self.get_user_info(access_token)
                # 判断用户信息是否存于数据库，
                # 如果存在，则返回一个 token
                # 不存在则将用户信息存入数据库，在生成一个token返回
                username = git_user_info.get('login')
                user_info = user.find({'username': username})
                if user_info:
                    return generate_token(user_info['_id'])
                else:
                    uid = user.insert({
                        "username": username,
                        "email": git_user_info.get('email', ''),
                        "avatar_url": git_user_info['avatar_url'],
                        "authority": "USER",
                    })
                    return generate_token(str(uid))
            else:
                return api_abort(403, 'Access denied, please try again.')
        else:
            return api_abort(403, 'Access denied, please try again.')


class User(Resource):

    method_decorators = {
        'get': [auth_required]
    }

    def get(self):
        print(g.user)
        return 'success'

    def post(self):
        """用户注册
        Args:
            username
            email
            password
        Return:
            {
                "token": token,
                "token_type": "JWT"
                "authority: 
            }
        """
        args = parser.parse(signup_args, request)

        if user.validate_user_exist({'email': args["email"]}):
            return api_abort(422, "Eamil已注册")
        elif user.validate_user_exist({'username': args["username"]}):
            return api_abort(422, "用户名已存在")

        user_info = {
            "username": args["username"],
            "email": args["email"].lower(),
            "password": args["password"],

        }
        user_id = user.insert(user_info)
        token = generate_token(str(user_id))

        data = {
            "token": token,
            "type": "Bearer",
        }
        headers = {
            "Cache-Control": "no-store",
            "Pragma": "no-cache"
        }
        resp = make_response(json.dumps(data))
        resp.headers.extend(headers or {})
        return resp
