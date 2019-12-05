# -*- coding: utf-8 -*-

import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
# WIN = sys.platform.startswith('win')
# if WIN:
#     prefix = 'sqlite:///'
# else:
#     prefix = 'sqlite:////'


class BaseConfig(object):

    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    # 邮件服务
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('NXGH', MAIL_USERNAME)
    APP_AUTHOR = os.getenv('APP_AUTHOR')
    APP_EMAIL = os.getenv('APP_EMAIL')

    # 文件存储目录
    APP_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    APP_ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


class DevelopmentConfig(BaseConfig):
    MONGO_URI = 'mongodb://blog_dev:password@localhost:27017/blog_dev'


class TestingConfig(BaseConfig):
    TESTING = True
    MONGO_URI = 'mongodb://rbac:password@localhost:20017/rbac'  


class ProductionConfig(BaseConfig):
    MONGO_URI = os.getenv('MONGODB_URI')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
