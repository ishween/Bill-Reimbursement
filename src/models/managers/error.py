
class ManagerError(Exception):
    """
        Class to handle exceptions
    """
    def __init__(self, message):
        self.message = message


class ManagerNotExistError(ManagerError):
    pass


class IncorrectPasswordError(ManagerError):
    pass
