import uuid
from src.db.database import Database
import src.models.billTypes.constants as billTypeConstant


class BillType(object):
    """
        Class to perform bill-type specific functionality
    """
    def __init__(self, department_id, type, reimbursement, _id=None):
        self.department_id = department_id
        self.type = type
        self.reimbursement = reimbursement
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Bill Type {}>".format(self.department_id, self.type, self.reimbursement)

    def add_bill_type(department_id, type, reimbursement):
        # to add bill-type by the admin of registered company
        BillType(department_id, type, reimbursement).save_to_db()

    def save_to_db(self):
        # to save data to the bill-type's database
        Database.insert(billTypeConstant.COLLECTION, self.json())

    def json(self):
        # creates the data structure
        return {
            "_id" : self._id,
            "department_id" : self.department_id,
            "type" : self.type,
            "reimbursement" : self.reimbursement
        }


    @classmethod
    def get_by_id(cls, _id):
        # get particular bill-type
        return cls(**Database.find_one(billTypeConstant.COLLECTION,{"_id":_id}))

    def delete(self):
        # delete a bill-type
        Database.delete(billTypeConstant.COLLECTION, {'_id':self._id})

    @classmethod
    def all_bills_type_by_department_id(cls, department_id):
        # get all bill-types of particular department
        billtypes = Database.find(billTypeConstant.COLLECTION, {'department_id':department_id})
        return billtypes

    @classmethod
    def all(cls, department_id):
        # get all bill-types from department
        return [cls(**elem) for elem in Database.find(billTypeConstant.COLLECTION, {'department_id':department_id})]

    def update_to_db(self):
        # update bill-type details
        Database.update(billTypeConstant.COLLECTION, {'_id':self._id}, self.json())

    def get_amount(department_id, type):
        # get amount reimburse for the bill type of a department
        return Database.find_one(billTypeConstant.COLLECTION, {'department_id': department_id, 'type':type})