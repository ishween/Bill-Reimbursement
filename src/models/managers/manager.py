import uuid
from src.db.database import Database
import src.models.managers.constants as managerConstants
import src.models.managers.error as ManagerError
from src.db.utils import Utils


class Manager(object):
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
        manager_data = Database.find_one(managerConstants.COLLECTION, {"email":email})

        if manager_data is None:
            raise ManagerError.ManagerNotExistError("You are not registered yet!")
        if not Utils.check_hashed_password(password, manager_data['password']):
            raise ManagerError.IncorrectPasswordError("You entered wrong password!")
        return True

    def add_a_manager(company_id, email, name, designation, department_id, date_of_joining):
        password = managerConstants.password_generator()
        Manager(company_id, email, Utils.hash_password(password), name, designation, department_id, date_of_joining).save_to_db()
        print(password)
        managerConstants.send_email(email, password)

    def save_to_db(self):
        Database.insert(managerConstants.COLLECTION, self.json())

    def json(self):
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
        print(Database.find_one(managerConstants.COLLECTION, {'_id': self._id}))
        Database.delete(managerConstants.COLLECTION, {'_id': self._id})

    @classmethod
    def get_by_id(cls, company_id):
        return Database.find(managerConstants.COLLECTION, {'company_id': company_id})

    @classmethod
    def get_by_manager_id(cls, _id):
        return cls(**Database.find_one(managerConstants.COLLECTION, {'_id': _id}))

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(managerConstants.COLLECTION, {})]

    def update_to_db(self):
        Database.update(managerConstants.COLLECTION, {'_id':self._id}, self.json())

    @classmethod
    def get_by_department_id(cls, department_id):
        managers = Database.find(managerConstants.COLLECTION, {'department_id': department_id})
        return managers

    @classmethod
    def get_by_manager_email(cls, email):
        employee = Database.find_one(managerConstants.COLLECTION, {'email': email})
        return employee