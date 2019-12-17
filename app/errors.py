from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def api_abort(code, message=None, **kwargs):
    if message is None:
        message = HTTP_STATUS_CODES.get(code, '')

    response = jsonify(code=code, message=message, **kwargs)
    response.status_code = code
    return response  # You can also just return (response, code) tuple


def invalid_token():
    response = api_abort(401, error='invalid_token',
                         error_description='Either the token was expired or invalid.')
    response.headers['WWW-Authenticate'] = 'Bearer'
    return response


def token_missing():
    response = api_abort(401, 'missing token')
    response.headers['WWW-Authenticate'] = 'Bearer'
    return response

class ValidationError(ValueError):
    pass

def register_exception(app):
    @app.errorhandler(ValidationError)
    def validation_error(e):
        return api_abort(400, e.args[0])

    @app.errorhandler(404)
    def page_not_found(e):
        return api_abort(404, 'The requested URL was not found on the server')

    @app.errorhandler(405)
    def method_not_allow(e):
        return api_abort(405, 'The method is not allow for the requested URL')

    @app.errorhandler(500)
    def server_error(e):
        return api_abort(500)
