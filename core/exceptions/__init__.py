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


@add_status_code(401)
class ValidationErrorException(SanicException):
    def __init__(self):
        message = 'Validation error exception'
        super().__init__(message)


@add_status_code(404)
class UserIdDoesNotExistInHeaderException(SanicException):
    def __init__(self):
        message = 'User id does not exist in header exception'
        super().__init__(message)


@add_status_code(404)
class NotFoundErrorException(SanicException):
    def __init__(self):
        message = 'Not found error exception'
        super().__init__(message)


@add_status_code(404)
class UploadErrorException(SanicException):
    def __init__(self):
        message = 'Upload error exception'
        super().__init__(message)


@add_status_code(404)
class CreateRowException(SanicException):
    def __init__(self):
        message = 'Create row exception'
        super().__init__(message)
