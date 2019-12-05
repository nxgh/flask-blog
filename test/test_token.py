# hack
import os
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from app.models.user import user
from app.auth import (
    generate_token,
    validate_token,
    get_token,
)
from app.extension import mongo
from app import create_app
from flask import url_for
import unittest




class TokenTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.runner = self.app.test_cli_runner()

        # mongo.db.create_collection('users')
        user.insert({
            'username': '测试用户',
            'password': 'Password_11&Test',
            'email': 'test1@gamil.com'
        })

    def tearDown(self):
        mongo.db.drop_collection('users')
        mongo.db.drop_collection('posts')

    def test_app_exsit(self):
        self.assertFalse(self.app is None)

    def test_app_testing(self):
        self.assertTrue(self.app.config['TESTING'])

    def test_generate_and_validate_token(self):
        object_id = "5de675e4cc14c528f2e98969"
        token = generate_token(object_id)
        self.assertTrue(type(token) == str)
        self.assertTrue(validate_token(token)['res'] == object_id)

    def test_register(self):
        resp = self.client.post(
            '/user',
            json={
                'username': 'testusser',
                'email': 'test1@foxmail.com',
                'password': 'test_1101&User'
            }
        )
        self.assertEqual(resp.status_code, 200)

        existuser = self.client.post(
            '/user',
            json={
                'username': 'existuser',
                'email': 'test1@foxmail.com',
                'password': 'test_1101&User'
            }
        )
        self.assertEqual(existuser.status_code, 422)

        illegal_pwd = self.client.post(
            '/user',
            json={
                'username': 'illegalpwd',
                'email': 'illegal_pwd@foxmail.com',
                'password': 'test1101ser'
            }
        )
        self.assertEqual(illegal_pwd.status_code, 422)

    def test_login(self):
        login = self.client.post(
            '/token',
            json={
                'email': 'test1@gamil.com',
                'password': 'Password_11&Test',

            }
        )
        print("login", type(login.get_data()))

    def test_authority(self):
        authority_resp = self.client.get('/token')
        print(f'authority_resp{authority_resp}')

if __name__ == "__main__":
    unittest.main()
