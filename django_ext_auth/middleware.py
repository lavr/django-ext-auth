import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser
from django.db.models import ObjectDoesNotExist
from django.utils.functional import SimpleLazyObject

from .utils import get_real_ip


class ExtAuthMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda: self.get_ext_user(request))

    def get_ext_user(self, request):
        assert(settings.EXTAUTH_AUTH_URL, "ExtAuthMiddleware requires settings.EXTAUTH_AUTH_URL")
        sessionid = settings.EXTAUTH_SESSIONID_COOKIE_NAME
        value = request.cookies.get(sessionid)
        r = requests.get(settings.EXTAUTH_AUTH_URL,
                         params={settings.EXTAUTH_SESSIONID_COOKIE_NAME: value,
                                 'userip': get_real_ip(),
                                 'app': settings.EXTAUTH_APP_NAME},
                         timeout=settings.EXTAUTH_AUTH_TIMEOUT)
        r.raise_for_status()
        user_data = r.json()['user']

        user = None
        try:
            user = get_user_model().objects.get(pk=user_data['id'])
        except ObjectDoesNotExist:
            if settings.EXTAUTH_CREATE_USER_ON_ACCESS:
                del user_data['id']
                user = get_user_model().objects.create(password=make_password(None),
                                                       **user_data)

        return user or AnonymousUser()
