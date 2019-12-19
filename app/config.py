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
    APP_AUTHOR = os.getenv('APP_AUTHOR')
    APP_EMAIL = os.getenv('APP_EMAIL')

    # 邮件服务

    MAIL_SERVER = os.getenv('MAIL_SERVER','')
    MAIL_PORT = os.getenv('MAIL_PORT', 587)
    MAIL_USE_SSL = True
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')

    # 使用 sendgrid 配置
    # MAIL_USE_TLS = True
    # MAIL_PASSWORD = os.getenv('SENDGRID_API_KEY')

    # 文件存储目录
    APP_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    APP_ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    MONGODB_DB = os.getenv('MONGODB_DB', 'blog_dev')
    MONGODB_HOST = os.getenv('MONGODB_HOST', '127.0.0.1')
    MONGODB_PORT = int(os.getenv('MONGODB_PORT', 27017))
    MONGODB_USERNAME = os.getenv('MONGODB_USERNAME', 'blog_dev')
    MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', 'password')


class TestingConfig(BaseConfig):
    TESTING = True
    MONGODB_DB = os.getenv('MONGODB_DB', 'test')
    MONGODB_HOST = os.getenv('MONGODB_HOST', '127.0.0.1')
    MONGODB_PORT = int(os.getenv('MONGODB_PORT', 20017))
    MONGODB_USERNAME = os.getenv('MONGODB_USERNAME', 'test')
    MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', 'password')


class ProductionConfig(BaseConfig):
    MONGODB_DB = os.getenv('MONGODB_DB','')
    MONGODB_HOST = os.getenv('MONGODB_HOST','')
    MONGODB_PORT = int(os.getenv('MONGODB_PORT', 0))
    MONGODB_USERNAME = os.getenv('MONGODB_USERNAME', '')
    MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', '')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
