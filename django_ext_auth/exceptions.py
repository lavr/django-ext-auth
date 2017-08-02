
class BaseException(Exception):
    pass


class Recoverable(BaseException):
    pass


class Permanent(BaseException):
    pass


class AuthNotAvailable(Recoverable):
    pass


class LocalUserDoesNotExist(Permanent):
    pass


class Unauthorized(Permanent):
    pass


