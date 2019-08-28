import unittest

from flask import url_for, current_app
from app import create_app
from app.extension import mongo
from app.resource.user.models import user


class UserTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.app_context = app.test_request_context()
        self.app_context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()

        # 初始化数据库
        user.insert({
            "username": "test1",
            "password": "password1",
            "email": "direnjie@gamil.com",
        })
        
    def tearDown(self):
        mongo.db.user.drop()
        self.app_context.pop()

    def test_404_response(self):
        response = self.client.get('/anoexisturl')
        status_code = response.status_code
        self.assertEqual(status_code, 404)

    def test_405_response(self):
        response = self.client.delete('/index')
        status_code = response.status_code
        self.assertEqual(status_code, 405)
    
    def test_user_signup(self):
        response = self.client.post(
            url_for('user_bp.user'),
            json = dict(
                username="test2",
                password="password2",
                email="test2@163.com",
                location="西安"
            )
        )
        status_code = response.status_code
        self.assertEqual(status_code, 201)
        
        response_422 = self.client.post(
            url_for('user_bp.user'),
            json = dict(
                username="test2",
                password="password2",
                email="direnjie@gamil.com",
                location="西安"
            )
        )
        status_code = response_422.status_code
        self.assertEqual(status_code, 422)

