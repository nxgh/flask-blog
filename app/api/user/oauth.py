import json
import os

import requests
from flask import request, make_response, current_app, g
from flask_restful import Resource

from app.errors import api_abort
from app.models.user import User
from app.api.auth import generate_token, permission_required
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

    def get(self):
        '''
            variable r   
            Success:
              {'access_token': '374171064616b9c53adb9149c356954ec3bf4199', 'token_type': 'bearer', 'scope': ''}
            Exception:
              {'error': 'bad_verification_code', 'error_description': 'The code passed is incorrect or expired.', 'error_uri': 'https://developer.github.com/apps/managing-oauth-apps/troubleshooting-oauth-app-access-token-request-errors/#bad-verification-code'}
        '''
        code = request.args.get('code', '')
        if code == '':
            return api_abort(403, 'Access denied, please try again.')
        try:
            request_assess_token_url = f'https://github.com/login/oauth/access_token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&code={code}'
            request_assess_token_headers = {'accept': 'application/json'}
            print(request_assess_token_url)
            r = requests.post(request_assess_token_url, headers=request_assess_token_headers).json()
            print(r)
        except Exception as e:
            current_app.logger.error(e)
            return api_abort(500, 'Requests Github Access Token Error')
        current_app.logger.info(f'request github access_token: {r}')
        if not r.get('access_token', None):
            return api_abort(401, 'The code passed is incorrect or expired.')

        request_user_info_url = 'https://api.github.com/user'
        request_user_info_headers={
            'accept': 'application/json',
            'Authorization': 'token ' + r['access_token']
        }
        try:
            user_info = requests.get(request_user_info_url, headers=request_user_info_headers).json()
            current_app.logger.info(f'requests github user_info: {user_info}')
            # return user_info
        except Exception as e:
            current_app.logger.error(e)
            return api_abort(400)

        username = user_info.get('login')
        # current_app.logger.info(u)
        u = User.objects(username=username).first()
        if u:
            return generate_token(u.id)
        else:
            user = User(
                username = username,
                email = user_info.get('email', ''),
                avatar = user_info.get('avatar_url', '')
            )
            user.save()
            uid = User.objects(username=username).first()
            current_app.logger.info(uid)
    
            return generate_token(uid)
