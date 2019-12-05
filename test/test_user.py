# hack
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from flask import url_for

from app import create_app
from app.extension import mongo
from app.auth import (
    generate_token,
    validate_token, 
    get_token,
)

class TokenTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.runner = self.app.test_cli_runner()

        mongo.db.create_collection('users')
        mongo.db.create_collection('posts')

    def tearDown(self):
        mongo.db.drop_collection('users')
        mongo.db.drop_collection('posts')

    def test_app_exsit(self):
        self.assertFalse(self.app is None)

    
        
if __name__ == "__main__":
    unittest.main()