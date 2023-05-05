from core.exceptions.app import CoreException


class UserException(CoreException):
    """
    Base User Exception
    """


class UserDoesNotExistException(UserException):
    """
    The user object does not exist (not found user id, username, etc...)
    """
