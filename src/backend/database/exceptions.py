class DatabaseException(Exception):
    pass


class EmailAddressAlreadyInUseException(DatabaseException):
    pass


class InvalidEmailAddressException(DatabaseException):
    pass


class InvalidPasswordException(DatabaseException):
    pass


class AuthenticationException(DatabaseException):
    pass


class UnknownUserException(AuthenticationException):
    pass

class WrongPasswordException(AuthenticationException):
    pass