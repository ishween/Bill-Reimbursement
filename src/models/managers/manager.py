import uuid
from src.db.database import Database
import src.models.managers.constants as managerConstants
import src.models.managers.error as ManagerError
from src.db.utils import Utils


class Manager(object):
    """
        Class to perform manager specific functionality
    """
    def __init__(self, company_id, email, password, name, designation, department_id, date_of_joining, _id=None):
        self.company_id = company_id
        self.email = email
        self.password = password
        self.name = name
        self.designation = designation
        self.department_id = department_id
        self.date_of_joining = date_of_joining
        self._id = uuid.uuid4().hex if _id is None else _id

    def is_login_valid(email, password):
        # """
        # checks if the entered credentials exist in database
        # :param email: user entered
        # :param password: user entered
        # :raises: Manager not exist, incorrect password exception
        # :return: True
        # """

        manager_data = Database.find_one(managerConstants.COLLECTION, {"email":email})

        if manager_data is None:
            raise ManagerError.ManagerNotExistError("You are not registered yet!")
        if not Utils.check_hashed_password(password, manager_data['password']):
            raise ManagerError.IncorrectPasswordError("You entered wrong password!")
        return True

    @classmethod
    def is_reset_password_valid(cls, email, old_password):
        # """
        # It checks whether the credentials are valid and exist
        # :param email: user email
        # :param old_password: user entered
        # :raise: Incorrect password exception
        # :return: manager's data
        # """
        manager_data = Database.find_one(managerConstants.COLLECTION, {'email': email})
        print(manager_data['password'])
        if not Utils.check_hashed_password(old_password, manager_data['password']):
            raise ManagerError.IncorrectPasswordError("Password does not match")

        return cls(**manager_data)

    def add_a_manager(company_id, email, name, designation, department_id, date_of_joining):
        # to add manager by the admin of registered company
        password = managerConstants.password_generator()
        Manager(company_id, email, Utils.hash_password(password), name, designation, department_id, date_of_joining).save_to_db()
        print(password)
        managerConstants.send_email(email, password)

    def save_to_db(self):
        # to save data to the manager's database
        Database.insert(managerConstants.COLLECTION, self.json())

    def json(self):
        # creates the data structure
        return {
            "_id": self._id,
            "company_id": self.company_id,
            "email": self.email,
            "password": self.password,
            "name": self.name,
            "designation": self.designation,
            "department_id": self.department_id,
            "date_of_joining": self.date_of_joining
        }

    def delete(self):
        # delete a manager by the admin
        # print(Database.find_one(managerConstants.COLLECTION, {'_id': self._id}))
        Database.delete(managerConstants.COLLECTION, {'_id': self._id})

    @classmethod
    def get_by_id(cls, company_id):
        # given the company ID, it returns the manager details of that company
        return Database.find(managerConstants.COLLECTION, {'company_id': company_id})

    @classmethod
    def get_by_manager_id(cls, _id):
        # given the manager's ID and returns the particular manager's details
        return cls(**Database.find_one(managerConstants.COLLECTION, {'_id': _id}))

    @classmethod
    def all(cls):
        # to get all managers
        return [cls(**elem) for elem in Database.find(managerConstants.COLLECTION, {})]

    def update_to_db(self):
        # to update particular manager details
        Database.update(managerConstants.COLLECTION, {'_id':self._id}, self.json())

    @classmethod
    def get_by_department_id(cls, department_id):
        # to get managers of particular department
        managers = Database.find(managerConstants.COLLECTION, {'department_id': department_id})
        return managers

    @classmethod
    def get_by_manager_email(cls, email):
        # to get employees from manager's email
        employee = Database.find_one(managerConstants.COLLECTION, {'email': email})
        return employee