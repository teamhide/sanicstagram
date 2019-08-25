from sanic.exceptions import SanicException, add_status_code


@add_status_code(400)
class TokenHeaderException(SanicException):
    def __init__(self):
        message = 'Token header exception'
        super().__init__(message)


@add_status_code(400)
class TokenDecodeErrorException(SanicException):
    def __init__(self):
        message = 'Token decode error exception'
        super().__init__(message)


@add_status_code(401)
class InvalidTokenException(SanicException):
    def __init__(self):
        message = 'Invalid token exception'
        super().__init__(message)
