class DatabaseException(Exception):
    pass


class InvalidRoleException(DatabaseException):
    def __init__(self):
        super().__init__('Invalid role')


class InvalidPasswordException(DatabaseException):
    def __init__(self):
        super().__init__('Invalid password')


class AuthenticationException(DatabaseException):
    pass


class UnknownUserException(AuthenticationException):
    def __init__(self):
        super().__init__('Unknown user')


class UnknownSalesEventException(DatabaseException):
    def __init__(self):
        super().__init__('Unknown sales event')


class UnknownItemException(DatabaseException):
    def __init__(self):
        super().__init__('Unknown item')


class UnauthorizedItemChangeException(DatabaseException):
    def __init__(self):
        super().__init__('Unauthorized change')


class WrongPasswordException(AuthenticationException):
    def __init__(self):
        super().__init__('Wrong password')


class InvalidEventTimeInterval(DatabaseException):
    def __init__(self):
        super().__init__('Start time and end time do not form valid interval')


class EmptySaleIsInvalid(DatabaseException):
    def __init__(self):
        super().__init__('Sale should at least have one item')


class DuplicateItemsInSale(DatabaseException):
    def __init__(self):
        super().__init__('Item occurs multiple times in sale')
