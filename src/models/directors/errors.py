class DirectorError(Exception):
    """
        Class to handle exceptions
    """
    def __init__(self, message):
        self.message = message


class DirectorNOtExistError(DirectorError):
    """ Inherited class from DirectorError"""
    pass


class IncorrectPasswordError(DirectorError):
    """ Inherited class from DirectorError"""
    pass
