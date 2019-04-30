"""Module defining exceptions."""
BAD_REQUEST = 400
NOT_AUTHORIZED = 401


class InvalidMail(Exception):
    """ Invalid mail exception is raised when you enter a bad email"""

    def __init__(self):
        super().__init__()
        self.message = 'Invalid mail. It should be like name@example.com'
        self.code = BAD_REQUEST


class SignedMail(Exception):
    """ Is raised when you enter a email that was already in the db"""
    def __init__(self):
        super().__init__()
        self.message = 'That mail is already registered'
        self.code = BAD_REQUEST


class InvalidOrganizationName(Exception):
    """
    Is raised when you enter an orga name
    longer than the permitted value
    """
    def __init__(self):
        super().__init__()
        self.message = "That organizations' name is too long."
        self.code = BAD_REQUEST


class InvalidToken(Exception):
    """ Is raised when a token doesn't belong to any user"""
    def __init__(self):
        super().__init__()
        self.message = 'User does not have access'
        self.code = NOT_AUTHORIZED


class InvalidCookie(Exception):
    """ Is raised when a token doesn't belong to any user"""
    def __init__(self):
        super().__init__()
        self.message = 'User does not have permission to perform action'
        self.code = NOT_AUTHORIZED


class UserNotRegistered(Exception):
    """ Is raised when a a user is not registered in firebase"""
    def __init__(self):
        super().__init__()
        self.message = 'User is not registered in firebase'
        self.code = NOT_AUTHORIZED


class SignedOrganization(Exception):
    """ Is raised when you enter a email that was already in the db"""
    def __init__(self):
        super().__init__()
        self.message = 'An organization with that name was already created'
        self.code = BAD_REQUEST