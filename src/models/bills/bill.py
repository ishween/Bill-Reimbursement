import uuid
from src.db.database import Database
import src.models.bills.constants as billConstant


class Bill(object):
    def __init__(self, employee_id, bill_type, department_id, date_of_submission, bill_image_url, status, _id=None):
        self.employee_id = employee_id
        self.bill_type = bill_type
        self.department_id = department_id
        self.date_of_submission = date_of_submission
        self.bill_image_url = bill_image_url
        self.status = status
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Bill {}>".format(self.bill_type, self.department_id, self.date_of_submission, self.bill_image_url)

    def add_bill(employee_id, bill_type, department_id, date_of_submission, bill_image_url):
        Bill(employee_id, bill_type, department_id, date_of_submission, bill_image_url, "pending").save_to_db()

    def save_to_db(self):
        Database.insert(billConstant.COLLECTION, self.json())

    def json(self):
        return {
            "_id": self._id,
            "employee_id": self.employee_id,
            "bill_type": self.bill_type,
            "department_id": self.department_id,
            "date_of_submission": self.date_of_submission,
            "bill_image_url": self.bill_image_url,
            "status": self.status
        }

    @classmethod
    def delete(cls, bill_id):
        Database.delete(billConstant.COLLECTION, {'_id': bill_id})

    @classmethod
    def get_by_id(cls, _id):
        return cls(**Database.find_one(billConstant.COLLECTION, {'_id': _id}))

    @classmethod
    def all_bills(cls, department_id, status):
        return Database.find(billConstant.COLLECTION, {'department_id': department_id, 'status': status})

    @classmethod
    def all_bills_for_employee(cls, employee_id):
        return Database.find(billConstant.COLLECTION, {'employee_id': employee_id})

    def update_to_db(self):
        Database.update(billConstant.COLLECTION, {'_id': self._id}, self.json())