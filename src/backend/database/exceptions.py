class DatabaseException(Exception):
    pass


class EmailAddressAlreadyInUseException(DatabaseException):
    pass


class InvalidPasswordException(DatabaseException):
    pass
