import random
import click
from flask import Flask
from faker import Faker

from app.models.user import User, Permission
from app.models.blog import Comment, Post
from app.models.question import Question, Answer
from app.extension import db

fake = Faker('zh-CN')


def register_cli(app):
    @app.cli.command('hello', help="print help")
    @click.argument('name')
    def hello(name):
        print("hello", name)

    @app.cli.command()
    def initdb():
        click.echo('Initializing the database...')
        User.drop_collection()
        Post.drop_collection()
        Question.drop_collection()


        click.echo('Generating the User..')
        # FIXME:
        for i in range(1, 10):
            u = User(
                email = fake.email(),
                username = fake.name(),
                avatar = f'http://192.168.1.106:8000/avatar/r{i}.png'
            )
            u.set_password('helloworld')
            u.save()
        click.echo('Done')

        click.echo('Generating the Post..')
        for i in range(10):
            p = Post(
                title = fake.sentence(),
                content = fake.text(2000),
                category = random.choices(['Python', 'JavaScript','Golang', 'Flask','Vue', 'Django'])[0],
                tags = random.choices(['Python', 'JavaScript','Golang', 'Flask','Vue', 'Django']),
            )
            p.save()
        click.echo('Done')
        
        click.echo('Generating the Comment..')
        for i in Post.objects.all():
            for j in range(5):
                c = Comment(
                    author = random.choice(User.objects.all()),
                    content = fake.text(200),
                    )
                i.comments.append(c)
                i.save()
        click.echo('Done')


        click.echo('Generating the Reply..')
        for i in Post.objects.all():
            for j in range(5):
                c = Comment(
                    author = random.choice(User.objects.all()),
                    content = fake.text(200),
                    reply = random.choice(i.comments).cid
                )
                i.comments.append(c)
                i.save()

        click.echo('Done')

        click.echo('Generating the Question..')
       
        for j in range(5):
            q = Question(
                title = fake.sentence(),
                author = random.choice(User.objects.all()),
                description = fake.text(200),
                tags = random.choices(['Python', 'JavaScript','Golang', 'Flask','Vue', 'Django']),
            )
            q.save()

        click.echo('Done')

        click.echo('Generating the Answer Comment..')
        for i in Question.objects.all():
            for j in range(5):
                c = Answer(
                    author = random.choice(User.objects.all()),
                    content = fake.text(200),
                    )
                i.answer.append(c)
                i.save()
        click.echo('Done')


        click.echo('Generating the Answer Reply..')
        for i in Question.objects.all():
            for j in range(5):
                c = Answer(
                    author = random.choice(User.objects.all()),
                    content = fake.text(200),
                    reply = random.choice(i.answer)._id
                )
                i.answer.append(c)
                i.save()

        click.echo('Done')
