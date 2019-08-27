from functools import wraps

import jwt

from core.exceptions import (TokenHeaderException, TokenDecodeErrorException,
                             InvalidTokenException,
                             UserIdDoesNotExistInHeaderException)
from core.settings import get_config


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


def extract_user_id_from_header():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            try:
                user_id = request.headers.get('sanicstagram-user-id')
                if not user_id:
                    raise UserIdDoesNotExistInHeaderException
                request['user_id'] = user_id
                return await f(request, *args, **kwargs)
            except (IndexError, AttributeError):
                raise TokenHeaderException
        return decorated_function
    return decorator


def extract_user_id_from_token():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            try:
                token = request.headers.get('Authorization').split('Bearer ')[1]
            except (IndexError, AttributeError):
                raise TokenHeaderException

            try:
                decoded_token = jwt.decode(
                    token,
                    get_config().jwt_secret_key,
                    algorithms=[get_config().jwt_algorithm],
                )
            except jwt.exceptions.DecodeError:
                raise TokenDecodeErrorException
            except jwt.exceptions.InvalidTokenError:
                raise InvalidTokenException

            try:
                user_id = decoded_token['user_id']
            except KeyError:
                raise InvalidTokenException

            request['user_id'] = user_id
            return await f(request, *args, **kwargs)
        return decorated_function
    return decorator
