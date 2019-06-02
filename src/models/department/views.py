from src.models.department.department import Department
from flask import render_template, request, Blueprint
from src.models.admins.views import get_by_email_company_id
import src.decorators as department_decorator

department_blueprint = Blueprint('department', __name__)


def add_department(company_id, name):
    # add a department
    Department.add_department(company_id, name)


@department_blueprint.route('/viewDepartments', methods=['GET'])
@department_decorator.requires_login
def view_departments_admin():
    # Displays departments of the company to the admin
    company_id = get_by_email_company_id()
    departments = Department.get_all(company_id)
    return render_template('admins/show_departments.html', departments=departments)


@department_blueprint.route('/addDepartment', methods=['GET', 'POST'])
@department_decorator.requires_login
def add_a_department():
    # Admin add a department of the company
    if request.method == 'POST':
        company_id = get_by_email_company_id()
        name = request.form['name']

        # add_department(company_id, name)
        Department.add_department(company_id, name)
    return render_template('admins/add_department.html')


def view_departments(company_id):
    # Display all departments of the company
    print(company_id)
    departments = Department.get_all(company_id)
    return departments


def get_department(department_id):
    # to get particular department
    department = Department.get_by_id(department_id)
    return department
