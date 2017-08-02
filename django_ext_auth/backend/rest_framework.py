import re

from ..tokens import get_user_for_token
from ..utils import get_real_ip


class BaseAuthentication(object):

    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        raise NotImplementedError(".authenticate() must be overridden.")

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        pass


class Token(BaseAuthentication):

    auth_rx = re.compile(r"^Bearer (.+)$")

    def authenticate(self, request):
        if "HTTP_AUTHORIZATION" not in request.META:
            return None

        token_rx_match = self.auth_rx.search(request.META["HTTP_AUTHORIZATION"])
        if not token_rx_match:
            return None

        token = token_rx_match.group(1)
        user = get_user_for_token(token, user_ip=get_real_ip(request))

        return (user, token)

    def authenticate_header(self, request):
        return 'Bearer realm="api"'
