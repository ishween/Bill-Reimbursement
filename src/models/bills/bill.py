import uuid
from src.db.database import Database
import src.models.bills.constants as billConstant
import src.models.bills.error as billError
import matplotlib.pyplot as plt


class Bill(object):
    def __init__(self, employee_id, manager_id, bill_type, department_id, date_of_submission, bill_image_url, status, _id=None):
        self.employee_id = None
        self.manager_id = None
        if employee_id is not None:
            self.employee_id = employee_id
        else:
            self.manager_id = manager_id
        self.bill_type = bill_type
        self.department_id = department_id
        self.date_of_submission = date_of_submission
        self.bill_image_url = bill_image_url
        self.status = status
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Bill {}>".format(self.bill_type, self.department_id, self.date_of_submission, self.bill_image_url)

    def add_bill(bill_type, employee_id, manager_id, department_id, date_of_submission, bill_image_url):
        Bill(employee_id, manager_id, bill_type, department_id, date_of_submission, bill_image_url, "pending").save_to_db()

    def save_to_db(self):
        if self.employee_id is not None:
            Database.insert(billConstant.COLLECTION, self.employee_json())
        else:
            Database.insert(billConstant.COLLECTION, self.manager_json())

    def employee_json(self):
        return {
            "_id": self._id,
            "employee_id": self.employee_id,
            "manager_id": self.manager_id,
            "bill_type": self.bill_type,
            "department_id": self.department_id,
            "date_of_submission": self.date_of_submission,
            "bill_image_url": self.bill_image_url,
            "status": self.status
        }

    def manager_json(self):
        return {
            "_id": self._id,
            "employee_id": self.employee_id,
            "manager_id": self.manager_id,
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

    def get_by_id_for_manager(_id):
        return Database.find_one(billConstant.COLLECTION, {'_id':_id})

    def update(_id, bill_type, employee_id, manager_id, department_id, date_of_submission, bill_image_url, status):
        response = {}
        response['bill_type'] = bill_type
        if employee_id is None:
            response['manager_id'] = manager_id
        else:
            response['employee_id'] = employee_id
        response['department_id'] = department_id
        response['date_of_submission'] = date_of_submission
        response['bill_image_url'] = bill_image_url
        response['status'] = status
        Database.update(billConstant.COLLECTION, {'_id':_id}, response)


    @classmethod
    def all_bills(cls, department_id, status):
        return Database.find(billConstant.COLLECTION, {'department_id': department_id, 'status': status})

    @classmethod
    def all_bills_for_employee(cls, employee_id):
        return Database.find(billConstant.COLLECTION, {'employee_id': employee_id})

    @classmethod
    def all_bills_for_employee_filter(cls, employee_id, filter_type):
        return Database.find(billConstant.COLLECTION, {'employee_id': employee_id, 'status': filter_type})

    @classmethod
    def all_bills_for_manager(cls, manager_id):
        return Database.find(billConstant.COLLECTION, {'manager_id': manager_id})

    @classmethod
    def all_bills_for_manager_filter(cls, manager_id, filter_type):
        return Database.find(billConstant.COLLECTION, {'manager_id': manager_id, 'status': filter_type})

    def employee_update_to_db(self):
        Database.update(billConstant.COLLECTION, {'_id': self._id}, self.employee_json())

    def manager_update_to_db(self):
        print(self.manager_json())
        Database.update(billConstant.COLLECTION, {'_id':self._id}, self.manager_json())

    def isReimbursementAdded(reimbursement_amount):
        if reimbursement_amount == "":
            raise billError.ReimbursementAmountNotAdded("Add Reimbursement Amount")
        else:
            return True

    # def graph(accept, pending, reject):
    #
    #     labels = "Pending", "Accept", "Reject"
    #     sizes = [pending / 100, accept / 100, reject / 100]
    #     # print(sizes)
    #     fig1, ax1 = plt.subplots()
    #     ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
    #             shadow=True, startangle=90)
    #     ax1.axis('equal')
    #     plt.savefig('plot.png')