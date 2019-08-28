# -*- coding: utf-8 -*-

import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig(object):
    # 密钥
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')
    
    # SQLAlchemy 配置
    # SQLALCHEMY_ECHO = True
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_RECORD_QUERIES = True
    # 数据库查询允许最大时间
    # APP_SLOW_QUERY_THRESHOLD = 1

    # Debug 工具
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_ENABLED = 'app.debug'
    DEBUG_TB_PROFILER_ENABLED = True

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

    # 分页配置
    APP_POST_PER_PAGE = 10
    APP_MANAGE_POST_PER_PAGE = 15
    APP_COMMENT_PER_PAGE = 15

    
    # 文件存储目录
    APP_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    APP_ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


class DevelopmentConfig(BaseConfig):
    # SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')
    MONGO_URI = 'mongodb://herba_dev:password@localhost:27017/herba_dev'
    # WTF_CSRF_CHECK_DEFAULT = False,
    # WTF_CSRF_ENABLED = False,


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    MONGO_URI = 'mongodb://herba_test:password@localhost:27017/herba_test'  # 

class ProductionConfig(BaseConfig):
    MONGO_URI = os.getenv('MONGODB_URI')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
