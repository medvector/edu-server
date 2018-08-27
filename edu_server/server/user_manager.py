from .models import User
from django.db import models


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
