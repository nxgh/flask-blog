import os
import click
from flask import Flask, jsonify

from app.config import config
from app.extension import db, mail
from app.api import blog_bp, user_bp
from app.commands import register_cli
from app.logger import register_logging
from app.errors import register_exception

from app.models.user import User, Permission
from app.models.blog import Comment, Post
from app.models.question import Question, Answer

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('app')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_views(app)
    register_shell_context(app)
    register_logging(app)
    register_cli(app)
    register_exception(app)

    return app


def register_extensions(app):
    db.init_app(app)
    mail.init_app(app)


def register_views(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(user_bp)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User, Permission=Permission, Post=Post, Comment=Comment, Question=Question)
