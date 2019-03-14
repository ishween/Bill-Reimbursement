import uuid
from src.db.database import Database
from src.db.utils import Utils
import src.models.employees.constants as employeeConstants
import src.models.employees.error as EmployeeError


class Employee(object):
    def __init__(self, company_id, email, password, name, designation, department_id, date_of_joining, monthly_salary, _id=None):
        self.company_id = company_id
        self.email = email
        self.password = password
        self.name = name
        self.designation = designation
        self.department_id = department_id
        self.date_of_joining = date_of_joining
        self.monthly_salary = monthly_salary
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Employee {}>".format(self.email, self.department_id, self.designation, self.date_of_joining,
                                      self.monthly_salary)

    def is_login_valid(email, password):
        employee_data = Database.find_one(employeeConstants.COLLECTION, {'email': email})
        #print(employee_data['password'])

        if employee_data is None:
            raise EmployeeError.EmployeeNotExistError("You are not registered yet!")
        if not Utils.check_hashed_password(password, employee_data['password']):
            raise EmployeeError.IncorrectPasswordError("You entered wrong password!")
        return True

    def add_an_employee(company_id, email, name, designation, department_id, date_of_joining, monthly_salary):
        password = employeeConstants.password_generator()
        Employee(company_id, email, Utils.hash_password(password), name, designation, department_id, date_of_joining,
                 monthly_salary).save_to_db()
        employeeConstants.send_email(email, password)

    def save_to_db(self):
        Database.insert(employeeConstants.COLLECTION, self.json())

    def json(self):
        return {
            "_id": self._id,
            "company_id": self.company_id,
            "email": self.email,
            "password": self.password,
            "name": self.name,
            "designation": self.designation,
            "department_id": self.department_id,
            "date_of_joining": self.date_of_joining,
            "monthly_salary": self.monthly_salary
        }

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(employeeConstants.COLLECTION, {})]

    def delete(self):
        Database.delete(employeeConstants.COLLECTION, {'_id': self._id})

    @classmethod
    def get_by_id(cls, company_id):
        return Database.find(employeeConstants.COLLECTION,{"company_id":company_id})

    @classmethod
    def get_by_employee_id(cls, _id):
        return cls(**Database.find_one(employeeConstants.COLLECTION,{'_id':_id}))

    def update_to_db(self):
        Database.update(employeeConstants.COLLECTION, {'_id':self._id}, self.json())

    @classmethod
    def get_by_department_id(cls, department_id):
        return Database.find(employeeConstants.COLLECTION, {'department_id': department_id})

    @classmethod
    def get_by_employee_email(cls, email):
        employee = Database.find_one(employeeConstants.COLLECTION, {'email': email})
        return employee
