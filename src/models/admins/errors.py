__author__ = 'ishween'


class AdminErrors(Exception):
    def __init__(self, message):
        self.message = message


class CompanyAlreadyRegisteredError(AdminErrors):
    pass


class AdminNotExistsError(AdminErrors):
    pass


class IncorrectPasswordError(AdminErrors):
    pass


class AdminAlreadyRegisteredError(AdminErrors):
    pass


class InvalidEmailError(AdminErrors):
    pass
