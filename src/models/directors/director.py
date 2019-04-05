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
        self._id = _id if not None else uuid.uuid4().hex

    def is_login_valid(email, password):
        Director_data = Database.find_one(directorConstants.COLLECTION, {'email':email})

        if Director_data is None:
            raise DirectorErrors.DirectorNOtExistError("You are not registered yet!")
        if not Utils.check_hashed_password(password, Director_data['password']):
            raise DirectorErrors.IncorrectPasswordError("YOu entered wrong password")
        return True

    
