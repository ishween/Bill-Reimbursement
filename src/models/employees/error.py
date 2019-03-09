
class EmployeeError(Exception):
    def __init__(self, message):
        self.message = message


class EmployeeNotExistError(EmployeeError):
    pass


class IncorrectPasswordError(EmployeeError):
    pass
