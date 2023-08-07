class DatabaseException(Exception):
    pass


class EmailAddressAlreadyInUseException(DatabaseException):
    def __init__(self):
        super().__init__('Email address is already in use')


class InvalidEmailAddressException(DatabaseException):
    def __init__(self):
        super().__init__('Invalid email address')


class InvalidPasswordException(DatabaseException):
    def __init__(self):
        super().__init__('Invalid password')


class AuthenticationException(DatabaseException):
    pass


class UnknownUserException(AuthenticationException):
    def __init__(self):
        super().__init__('Unknown user')

class WrongPasswordException(AuthenticationException):
    def __init__(self):
        super().__init__('Wrong password')


class InvalidEventTimeInterval(DatabaseException):
    def __init__(self):
        super().__init__('Start time and end time do not form valid interval')
