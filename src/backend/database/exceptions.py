class DatabaseException(Exception):
    pass


class EmailAddressAlreadyInUseException(DatabaseException):
    def __init__(self):
        super().__init__('email address already in use')


class InvalidEmailAddressException(DatabaseException):
    def __init__(self):
        super().__init__('invalid email address')


class InvalidPasswordException(DatabaseException):
    def __init__(self):
        super().__init__('invalid password')


class AuthenticationException(DatabaseException):
    pass


class UnknownUserException(AuthenticationException):
    def __init__(self):
        super().__init__('unknown user')

class WrongPasswordException(AuthenticationException):
    def __init__(self):
        super().__init__('wrong password')