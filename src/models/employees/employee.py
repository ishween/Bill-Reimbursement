import uuid
from src.db.database import Database
from src.db.utils import Utils
import src.models.employees.constants as employeeConstants
import src.models.employees.error as EmployeeError


class Employee(object):
    """
        Class to perform employee specific functionality
    """
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
        # """
        # checks if the entered credentials exist in database
        # :param email: user entered
        # :param password: user entered
        # :raises: Employee not exist, incorrect password exception
        # :return: True
        # """
        employee_data = Database.find_one(employeeConstants.COLLECTION, {'email': email})

        if employee_data is None:
            raise EmployeeError.EmployeeNotExistError("You are not registered yet!")
        if not Utils.check_hashed_password(password, employee_data['password']):
            raise EmployeeError.IncorrectPasswordError("You entered wrong password!")
        return True

    @classmethod
    def is_reset_password_valid(cls,email, old_password):
        # """
        # It checks whether the credentials are valid and exist
        # :param email: user email
        # :param old_password: user entered
        # :raise: Incorrect password exception
        # :return: employee's data
        # """
        employee_data = Database.find_one(employeeConstants.COLLECTION, {'email':email})
        print(employee_data['password'])
        if not Utils.check_hashed_password(old_password, employee_data['password']):
            raise EmployeeError.IncorrectPasswordError("Password does not match")

        return cls(**employee_data)

    def add_an_employee(company_id, email, name, designation, department_id, date_of_joining, monthly_salary):
        # to add employee by the admin of registered company
        password = employeeConstants.password_generator()
        Employee(company_id, email, Utils.hash_password(password), name, designation, department_id, date_of_joining,
                 monthly_salary).save_to_db()
        employeeConstants.send_email(email, password)

    def save_to_db(self):
        # to save data to the employee's database
        Database.insert(employeeConstants.COLLECTION, self.json())

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
            "date_of_joining": self.date_of_joining,
            "monthly_salary": self.monthly_salary
        }

    @classmethod
    def all(cls):
        # to get all employees
        return [cls(**elem) for elem in Database.find(employeeConstants.COLLECTION, {})]

    def delete(self):
        # delete a employee by the admin
        Database.delete(employeeConstants.COLLECTION, {'_id': self._id})

    @classmethod
    def get_by_id(cls, company_id):
        # given the company ID, it returns the employee details of that company
        return Database.find(employeeConstants.COLLECTION,{"company_id":company_id})

    @classmethod
    def get_by_employee_id(cls, _id):
        print("Emp id:",_id)
        # given the employee's ID and returns the particular employee's details
        # return cls(**Database.find_one(employeeConstants.COLLECTION,{'_id':_id}))
        response = Database.find_one(employeeConstants.COLLECTION, {'_id': _id})
        print("he is mad", response)
        if response is None:
            return None
            # raise EmployeeError.EmployeeNotExistError
        else:
            print(cls(**response))
            return cls(**response)

    def update_to_db(self):
        # to update particular employee details
        Database.update(employeeConstants.COLLECTION, {'_id':self._id}, self.json())

    @classmethod
    def get_by_department_id(cls, department_id):
        # to get employees of particular department
        return Database.find(employeeConstants.COLLECTION, {'department_id': department_id})

    @classmethod
    def get_by_employee_email(cls, email):
        # to get employees from manager's email
        employee = Database.find_one(employeeConstants.COLLECTION, {'email': email})
        # print(employee)
        return employee
