# from typing import Any
# from urllib.parse import parse_qs

# from channels.auth import AuthMiddleware
from channels.db import database_sync_to_async
# from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
# from jwt import decode as jwt_decode
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken


@database_sync_to_async
def get_user_from_token(token: str):
    User = get_user_model()
    try:
        untyped_token = UntypedToken(token)
        # print("untyped_token: ", untyped_token)
        user = JWTAuthentication().get_user(untyped_token)
        # print("user: ", user)
        if user is not None:
            return user
        else:
            # No user associated with the JWT
            return AnonymousUser()
    except (InvalidToken, TokenError, User.DoesNotExist):
        print("user does not exist")
        return AnonymousUser()


class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        headers_dict = dict((k.decode(), v.decode()) for k, v in scope["headers"])
        # print(headers_dict)
        token = headers_dict.get("bearer", None)
        if token:
            scope["user"] = await get_user_from_token(token)
        else:
            scope["user"] = AnonymousUser()
        return await self.app(scope, receive, send)
