class DirectorError(Exception):
    def __init__(self, message):
        self.message = message

class DirectorNOtExistError(DirectorError):
    pass

class IncorrectPasswordError(DirectorError):
    pass
