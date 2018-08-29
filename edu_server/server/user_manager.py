from .models import User
from django.db import models
from datetime import datetime, timedelta


class UserManager:
    @staticmethod
    def create_user(tokens_info: dict, hub_user_info: dict) -> User:
        user = User.objects.create(login=hub_user_info['login'], hub_id=hub_user_info['id'],
                                   access_token=tokens_info['access_token'], refresh_token=tokens_info['refresh_token'],
                                   expires_in=tokens_info['expires_in'], token_type=tokens_info['token_type'])
        return user

    @staticmethod
    def update_user(user: User, tokens_info: dict, hub_user_info: dict) -> User:
        user.hub_id = hub_user_info['id']
        user.login = hub_user_info['login']

        user.access_token = tokens_info['access_token']
        user.refresh_token = tokens_info['refresh_token']
        user.expires_in = tokens_info['expires_in']
        user.token_type = tokens_info['token_type']

        user.save()
        return user

    @staticmethod
    def check_user_by_hub_id(hub_id: dict):
        try:
            user = User.objects.get(hub_id=hub_id)
        except models.ObjectDoesNotExist:
            return None

        return user

    def check_user_authorization(self, authorization_string: str):
        token_type, user_id, hub_token = self.split_authorization_string(authorization_string)
        user = User.objects.get(id=user_id)
        expiration_time = user.access_token_updated_at + timedelta(seconds=user.expires_in)
        return user.token_type == token_type and user.access_token == hub_token and datetime.now() <= expiration_time

    @staticmethod
    def split_authorization_string(authorization_string: str):
        token_type, token = authorization_string.split(' ')
        token = token.split('.')
        user_id = token[0]
        hub_token = '.'.join(token[1:])

        return token_type, user_id, hub_token

    def user_logout(self, authorization_string: str):
        token_type, user_id, hub_token = self.split_authorization_string(authorization_string)
        user = User.objects.get(id=user_id)
        user.expires_in = 0
        user.save()
        return True
