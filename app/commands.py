import click
from flask import Flask


def register_cli(app):
    @app.cli.command('hello', help="print help")
    @click.argument('name')
    def hello(name):
        print("hello", name)
