import os
# from flask_sqlalchemy import SQLAlchemy
# from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail
from flask_socketio import SocketIO
from flask_pymongo import PyMongo


# db = SQLAlchemy()
mongo = PyMongo()
socketio = SocketIO()
mail = Mail()
# toolbar = DebugToolbarExtension()

