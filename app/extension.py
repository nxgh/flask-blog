from flask_mail import Mail
from flask_mongoengine import MongoEngine

db = MongoEngine()

mail = Mail()
