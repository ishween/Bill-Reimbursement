import uuid
from src.db.database import Database
import src.models.bills.constants as billConstant


class Bill(object):
    def __init__(self, employee_id, bill_type, department_id, date_of_submission, bill_image, status, _id=None):
        self.employee_id = employee_id
        self.bill_type = bill_type
        self.department_id = department_id
        self.date_of_submission = date_of_submission
        self.bill_image = bill_image
        self.status = status
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Bill {}>".format(self.bill_type, self.department_id, self.date_of_submission, self.bill_image)

    def add_bill(employee_id, bill_type, department_id, date_of_submission, bill_image):
        Bill(employee_id, bill_type, department_id, date_of_submission, bill_image, "pending").save_to_db()

    def save_to_db(self):
        Database.insert(billConstant.COLLECTION, self.json())

    def json(self):
        return {
            "employee_id": self.employee_id,
            "bill_type": self.bill_type,
            "department": self.department_id,
            "date_of_submission": self.date_of_submission,
            "bill_image": self.bill_image,
            "status": self.status
        }

    def delete(self):
        Database.delete(billConstant.COLLECTION, {'_id': self._id})

    @classmethod
    def get_by_id(cls, _id):
        return cls(**Database.find_one(billConstant.COLLECTION, {'_id': _id}))

    @classmethod
    def all_bills(cls, department_id, status):
        return [cls(**elem) for elem in Database.find(billConstant.COLLECTION, {'department_id': department_id, 'status': status})]
