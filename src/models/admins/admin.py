import uuid
from src.db.database import Database
import src.models.admins.constants as adminConstant
import src.models.admins.errors as adminErrors
from src.db.utils import Utils


class Admin(object):
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
        """
        check company name if it exist then error
        check email exist if it exist then error
        :return: true if registered else false
        """
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

    def save_to_db(self):
        Database.insert(adminConstant.COLLECTION, self.json())

    def json(self):
        return {
            "company_name": self.company_name,
            "ceo": self.ceo,
            "email": self.email,
            "password": self.password,
            "contact": self.contact,
            "gst_no": self.gst_no
        }

    def is_login_valid(email, password):
        admin_data = Database.find_one(adminConstant.COLLECTION, {"email":email})

        if admin_data is None:
            raise adminErrors.AdminNotExistsError("You are not registered")
        if not Utils.check_hashed_password(password, admin_data['password']):
            raise adminErrors.IncorrectPasswordError("Your password is wrong")

        return True

    @classmethod
    def is_reset_password_valid(cls, email, old_password):
        admin_data = Database.find_one(adminConstant.COLLECTION, {'email': email})
        #print(manager_data['password'])
        if not Utils.check_hashed_password(old_password, admin_data['password']):
            raise adminErrors.IncorrectPasswordError("Password does not match")

        return cls(**admin_data)

    @classmethod
    def get_by_email(cls, email):
        company_id = Database.find_one(adminConstant.COLLECTION, {'email':email})['_id']
        return company_id

