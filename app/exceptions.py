"""Module defining exceptions."""


class InvalidMail(Exception):
    """ Invalid mail exception is raised when you enter a bad email"""

    def __init__(self):
        super().__init__()
        self.message = 'Invalid mail. It should be like name@example.com'


class SignedMail(Exception):
    """ Is raised when you enter a email that was already in the db"""
    def __init__(self):
        super().__init__()
        self.message = 'That mail is already registered'


class InvalidOrganizationName(Exception):
    """
    Is raised when you enter an orga name
    longer than the permitted value
    """
    def __init__(self):
        super().__init__()
        self.message = "That organizations' name is too long."
