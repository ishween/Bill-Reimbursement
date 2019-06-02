import uuid
from src.db.database import Database
import src.models.admins.constants as adminConstant
import src.models.admins.errors as adminErrors
from src.db.utils import Utils


class Admin(object):
    """
        Class to perform admin specific functionality
    """
    def __init__(self, company_name, ceo, email, password, contact, gst_no, _id=None):
        self.company_name = company_name
        self.ceo = ceo
        self.email = email
        self.password = password
        self.contact = contact
        self.gst_no = gst_no
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def register(company_name, ceo, email, password, contact, gst_no):
        # """
        # registers the company for bill reimbursement
        # :raises: company already registered, admin already registered
        # :return: true if successfully registered
        # """
        company_data = Database.find_one(adminConstant.COLLECTION, {"company_name":company_name})
        admin_data = Database.find_one(adminConstant.COLLECTION, {"email": email})

        if company_data is not None:
            raise adminErrors.CompanyAlreadyRegisteredError("Your company is already registered")
        if admin_data is not None:
            raise adminErrors.AdminAlreadyRegisteredError("You are already registered")
        if not Utils.email_is_valid(email):
            raise adminErrors.InvalidEmailError("You entered wrong email")
        Admin(company_name, ceo, email, Utils.hash_password(password), contact, gst_no).save_to_db()

        return True

    def is_login_valid(email, password):
        # """
        # Checks if the entered credentials exist in database
        # :param email: user entered
        # :param password: user entered
        # :raises: Admin not exist, incorrect password exception
        # :return: True
        # """
        admin_data = Database.find_one(adminConstant.COLLECTION, {"email":email})

        if admin_data is None:
            raise adminErrors.AdminNotExistsError("You are not registered")
        if not Utils.check_hashed_password(password, admin_data['password']):
            raise adminErrors.IncorrectPasswordError("Your password is wrong")

        return True

    def save_to_db(self):
        # to save data to the manager's database
        Database.insert(adminConstant.COLLECTION, self.json())

    def json(self):
        # creates the data structure
        return {
            "company_name": self.company_name,
            "ceo": self.ceo,
            "email": self.email,
            "password": self.password,
            "contact": self.contact,
            "gst_no": self.gst_no
        }

    @classmethod
    def is_reset_password_valid(cls, email, old_password):
        # """
        # It checks whether the credentials are valid and exist
        # :param email: user email
        # :param old_password: user entered
        # :raise: Incorrect password exception
        # :return: admins's data
        # """
        admin_data = Database.find_one(adminConstant.COLLECTION, {'email': email})
        #print(manager_data['password'])
        if not Utils.check_hashed_password(old_password, admin_data['password']):
            raise adminErrors.IncorrectPasswordError("Password does not match")

        return cls(**admin_data)

    @classmethod
    def get_by_email(cls, email):
        # to get company ID using admin's email
        company_id = Database.find_one(adminConstant.COLLECTION, {'email':email})['_id']
        return company_id

