import os
import click
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
from flask import Flask, jsonify


from app.config import config
from app.extension import mongo, mail
from app.resource import blog_bp, user_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('app')
    app.config.from_object(config[config_name])

    register_extensions(app)  # 扩展初始化
    register_views(app)  # 蓝图
    # register_commands(app) # 自定义shell命令
    register_shell_context(app)  # shell 上下文处理函数

    return app


def register_extensions(app):
    mongo.init_app(app)
    # toolbar.init_app(app)
    mail.init_app(app)


def register_views(app):
    # app.register_blueprint(api_v1, url_prefix='/api/v1')
    # app.register_blueprint(chat_bp, url_prefix='/chat')
    app.register_blueprint(blog_bp)
    app.register_blueprint(user_bp)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(mongo=mongo)
