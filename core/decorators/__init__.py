import jwt
from functools import wraps
from core.settings import get_config
from core.exceptions import (TokenHeaderException, TokenDecodeErrorException,
                             InvalidTokenException)


def is_jwt_authenticated():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            try:
                token = request.headers.get('Authorization').split('Bearer ')[1]
            except (IndexError, AttributeError):
                raise TokenHeaderException

            try:
                jwt.decode(
                    token,
                    get_config().jwt_secret_key,
                    algorithms=[get_config().jwt_algorithm],
                )
                response = await f(request, *args, **kwargs)
                return response
            except jwt.exceptions.DecodeError:
                raise TokenDecodeErrorException
            except jwt.exceptions.InvalidTokenError:
                raise InvalidTokenException
        return decorated_function
    return decorator
