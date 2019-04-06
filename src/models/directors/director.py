import uuid
from src.db.database import Database
from src.db.utils import Utils
import src.models.directors.constants as directorConstants
import src.models.directors.errors as DirectorErrors


class Director(object):
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
        director_data = Database.find_one(directorConstants.COLLECTION, {'email':email})

        if director_data is None:
            raise DirectorErrors.DirectorNOtExistError("You are not registered yet!")
        if not Utils.check_hashed_password(password, director_data['password']):
            raise DirectorErrors.IncorrectPasswordError("YOu entered wrong password")
        return True


    @classmethod
    def is_reset_password_valid(cls, email, old_password):
        director_data = Database.find_one(directorConstants.COLLECTION, {'email': email})
        print(director_data['password'])
        if not Utils.check_hashed_password(old_password, director_data['password']):
            raise DirectorErrors.IncorrectPasswordError("Password does not match")

        return cls(**director_data)

    def add_a_director(company_id, email, name, designation, department_id, date_of_joining):
        password = directorConstants.password_generator()
        Director(company_id, email, Utils.hash_password(password), name, designation, department_id, date_of_joining).save_to_db()
        print(password)
        directorConstants.send_email(email, password)

    def save_to_db(self):
        Database.insert(directorConstants.COLLECTION, self.json())

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
        print(Database.find_one(directorConstants.COLLECTION, {'_id': self._id}))
        Database.delete(directorConstants.COLLECTION, {'_id': self._id})

    @classmethod
    def get_by_id(cls, company_id):
        return Database.find(directorConstants.COLLECTION, {'company_id': company_id})

    @classmethod
    def get_by_director_id(cls, _id):
        return cls(**Database.find_one(directorConstants.COLLECTION, {'_id': _id}))

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(directorConstants.COLLECTION, {})]

    def update_to_db(self):
        Database.update(directorConstants.COLLECTION, {'_id':self._id}, self.json())

    @classmethod
    def get_by_department_id(cls, department_id):
        directors = Database.find(directorConstants.COLLECTION, {'department_id': department_id})
        return directors

    @classmethod
    def get_by_director_email(cls, email):
        director = Database.find_one(directorConstants.COLLECTION, {'email': email})
        return director