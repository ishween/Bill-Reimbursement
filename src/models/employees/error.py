
class EmployeeError(Exception):
    """
        Class to handle exceptions
    """
    def __init__(self, message):
        self.message = message


class EmployeeNotExistError(EmployeeError):
    pass


class IncorrectPasswordError(EmployeeError):
    pass
