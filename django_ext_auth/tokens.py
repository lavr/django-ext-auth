import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied
from django.contrib.auth.hashers import make_password
from .exceptions import Unauthorized, AuthNotAvailable, LocalUserDoesNotExist


def _load_userinfo(sessionid, user_ip):

    r = requests.get(settings.EXTAUTH_AUTH_URL,
                     params={settings.EXTAUTH_SESSIONID_COOKIE_NAME: sessionid,
                             'user_ip': user_ip,
                             'app': settings.EXTAUTH_APP_NAME},
                     timeout=settings.EXTAUTH_AUTH_TIMEOUT)

    if r.status_code == 200:
        return r.json()['user']

    if r.status_code in (401, 403):
        raise PermissionDenied

    # timeout or server error
    raise AuthNotAvailable()


def get_user_for_sessionid(sessionid, user_ip=None):

    user_data = _load_userinfo(sessionid, user_ip=user_ip)

    try:
        user = get_user_model().objects.get(username=user_data['username'])
    except ObjectDoesNotExist:
        if settings.EXTAUTH_CREATE_USER_ON_ACCESS:
            del user_data['id']
            user = get_user_model().objects.create(password=make_password(None),
                                                   **user_data)
        else:
            raise LocalUserDoesNotExist()

    return user


def get_user_for_token(token, user_ip=None, skip_invalid_token=True):
    try:
        return get_user_for_sessionid(sessionid=token, user_ip=user_ip)
    except PermissionDenied:
        if not skip_invalid_token:
            raise