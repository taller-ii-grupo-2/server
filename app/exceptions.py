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


class InvalidToken(Exception):
    """ Is raised when a token doesn't belong to any user"""
    def __init__(self):
        super().__init__()
        self.message = 'User does not have access'
        self.code = NOT_AUTHORIZED
