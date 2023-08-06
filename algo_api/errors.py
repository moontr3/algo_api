
class DefaultException(Exception):
    def __init__(self, message):
        super().__init__(message)

class UnknownException       (DefaultException): pass
class SessionClosed          (DefaultException): pass
class InvalidCredentials     (DefaultException): pass
class NotImplementedException(DefaultException): pass
class AlreadyLoggedIn        (DefaultException): pass