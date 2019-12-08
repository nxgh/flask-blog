import json
import os

import requests
from flask import request, make_response, current_app, g
from flask_restful import Resource

from app.errors import api_abort
from app.models.user import user
from app.api.auth import generate_token, admin_required, auth_required
from app.forms.user import signup_args

CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
REDIRECT_URL = os.getenv('GITHUB_REDIRECT_URL')
CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')


class GitToken(Resource):

    def get(self):
        '''返回用户跳转到 Github 的 Url
        URL 指向 GitHub 的 OAuth 授权网址
        '''
        base_url = 'https://github.com/login/oauth/authorize?'

        result = f'{base_url}client_id={CLIENT_ID}&redirect_uri={REDIRECT_URL}'
        return result


class GitUser(Resource):

    @staticmethod
    def get_access_token(code):
        base_url = 'https://github.com/login/oauth/access_token?'
        url = f'{base_url}client_id={CLIENT_ID}&client_secret={CLIENT_SECRET} \
            &code={code}'

        headers = {'accept': 'application/json'}
        '''r   
            Success:
              {'access_token': '374171064616b9c53adb9149c356954ec3bf4199', 'token_type': 'bearer', 'scope': ''}
            Exception:
              {'error': 'bad_verification_code', 'error_description': 'The code passed is incorrect or expired.', 'error_uri': 'https://developer.github.com/apps/managing-oauth-apps/troubleshooting-oauth-app-access-token-request-errors/#bad-verification-code'}
        '''
        try:
            r = requests.post(url, headers=headers).json()
        except Exception as e:
            current_app.logger.error(e)
            return api_abort(500, 'Requests Github Access Token Error')

        current_app.logger.info('请求github access_token: {0}'.format(r))

        if r.get('access_token', None):
            return r['access_token']
        else:
            return api_abort(401, 'The code passed is incorrect or expired.')

    @staticmethod
    def get_user_info(access_token):
        user_info = requests.get(
            'https://api.github.com/user',
            headers={
                'accept': 'application/json',
                'Authorization': 'token ' + access_token
            }
        ).json()
        current_app.logger.info(
            'requests github user_info: {0}'.format(user_info))
        return user_info

    def get(self):
        code = request.args.get('code', '')
        if code:
            access_token = self.get_access_token(
                code)  # token:  '374171064616b...'
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
                })
                return generate_token(uid)
        else:
            return api_abort(403, 'Access denied, please try again.')
