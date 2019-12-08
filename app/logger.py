from flask import request
import logging, os
from logging.handlers import RotatingFileHandler, SMTPHandler

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def register_logging(app):
    class RequestFormatter(logging.Formatter):

        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s \n'
        'requested %(url)s\n'
        'File %(pathname)s line %(lineno)d in %(funcName)s\n'
        'level - %(levelname)s - message %(message)s'
    )

    error_handler = RotatingFileHandler(
        os.path.join(basedir, 'logs/error.log'),
        maxBytes=10 * 1024 * 1024, backupCount=10)

    info_handler = RotatingFileHandler(
        os.path.join(basedir, 'logs/info.log'),
        maxBytes=10 * 1024 * 1024, backupCount=10)

    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)

    info_handler.setFormatter(formatter)
    info_handler.setLevel(logging.INFO)

    # mail_handler = SMTPHandler(
    #     mailhost=app.config['MAIL_SERVER'],
    #     fromaddr=app.config['MAIL_USERNAME'],
    #     toaddrs=['ADMIN_EMAIL'],
    #     subject='Bluelog Application Error',
    #     credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
    # mail_handler.setLevel(logging.ERROR)
    # mail_handler.setFormatter(request_formatter)

    # if not app.debug:
        # app.logger.addHandler(mail_handler)
    if app.debug:
        app.logger.addHandler(info_handler)
    app.logger.addHandler(error_handler)