from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from .tokens import get_user_for_sessionid
from .utils import get_real_ip


def get_user(request):
    assert settings.EXTAUTH_AUTH_URL, "ExtAuthMiddleware requires settings.EXTAUTH_AUTH_URL"
    sessionid = request.COOKIES.get(settings.EXTAUTH_SESSIONID_COOKIE_NAME)
    user = get_user_for_sessionid(sessionid, user_ip=get_real_ip(request))
    return user or AnonymousUser()


class ExtAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: get_user(request))
