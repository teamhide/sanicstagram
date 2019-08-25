import jwt
from sanic.request import Request

from core.exceptions import (TokenHeaderException, TokenDecodeErrorException,
                             InvalidTokenException)
from core.settings import get_config


class TokenHelper:
    @classmethod
    def extract_from_request(cls, request: Request):
        try:
            return request.headers.get('Authorization').split('Bearer ')[1]
        except (IndexError, AttributeError):
            raise TokenHeaderException

    @classmethod
    def decode(cls, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                get_config().jwt_secret_key,
                algorithms=[get_config().jwt_algorithm],
            )
        except jwt.exceptions.DecodeError:
            raise TokenDecodeErrorException
        except jwt.exceptions.InvalidTokenError:
            raise InvalidTokenException

    @classmethod
    def encode(cls, user_id: int):
        return jwt.encode(
            payload={'user_id': user_id},
            key=get_config().jwt_secret_key,
            algorithm=get_config().jwt_algorithm,
        )
