import uuid
from src.db.database import Database
import src.models.department.constants as departmentConstant
from src.models.admins.admin import Admin


class Department(object):
    def __init__(self, company_id, name, _id=None):
        self.company_id = company_id
        self.name = name
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Bill Type {}>".format(self.name)

    def add_department(company_id, name):
        Department(company_id, name).save_to_db()

    def save_to_db(self):
        Database.insert(departmentConstant.COLLECTION, self.json())

    def json(self):
        return {
            "_id" : self._id,
            "company_id" : self.company_id,
            "name" : self.name
        }

    @classmethod
    def get_by_id(cls, _id):
        return Database.find_one(departmentConstant.COLLECTION,{"_id":_id})

    @classmethod
    def get_all(cls, company_id):
        departments = Database.find(departmentConstant.COLLECTION, {'company_id':company_id})
        return departments

    @classmethod
    def all(cls, company_id):
        return [cls(**elem) for elem in Database.find(departmentConstant.COLLECTION, {"company_id": company_id})]
