from .models import User
from django.db import models
from datetime import datetime, timedelta, timezone
from urllib.error import HTTPError
import urllib.request
import base64
import json
from edu_server import settings
from edu_server.secret_settings import service_id, service_secret

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

    @staticmethod
    def refresh_access_token(user: User):
        req = urllib.request.Request(settings.HUB_OAUTH_API_BASE_URL + '/token', method='POST')
        req.add_header('Host', 'hub.jetbrains.com')
        service_info = service_id + ':' + service_secret
        b64_service_info = base64.b64encode(service_info.encode('utf-8')).decode()
        req.add_header("Authorization", "Basic %s" % b64_service_info)
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        grant = 'grant_type=refresh_token&refresh_token=' + user.refresh_token
        req.data = grant.encode()

        try:
            resp = urllib.request.urlopen(req)
        except HTTPError:
            return False

        tokens_info = json.loads(resp.read().decode('utf-8'))
        user.access_token = tokens_info['access_token']
        user.refresh_token = tokens_info['refresh_token']
        user.expires_in = tokens_info['expires_in']
        user.token_type = tokens_info['token_type']
        user.save()

        return True

    def check_user_authorization(self, authorization_string: str):
        token_type, user_id, hub_token = self.split_authorization_string(authorization_string)
        user = User.objects.get(id=user_id)
        expiration_time = user.access_token_updated_at + timedelta(seconds=user.expires_in)
        return user.token_type == token_type and user.access_token == hub_token \
               and datetime.now(timezone.utc) <= expiration_time

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
