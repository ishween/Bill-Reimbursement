from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
import src.models.employees.error as employeeErrors
from src.models.employees.employee import Employee

__author__ = 'ishween'

employee_blueprint = Blueprint('employees', __name__)


@employee_blueprint.route('/employee/login', methods=['GET', 'POST'])
def login_employee():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if Employee.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for('bills.view_bills', sort_type="default", filter_type="all"))
        except employeeErrors.EmployeeError as a:
            return a.message

    return render_template('employees/login_employee.html')


@employee_blueprint.route('/employee', methods=['GET'])
def to_menu():
    return render_template('employees/view_bills.html')


def add_an_employee(company_id, email, name, designation, department_id, date_of_joining, monthly_salary):
    Employee.add_an_employee(company_id, email, name, designation, department_id, date_of_joining, monthly_salary)


@employee_blueprint.route('/employee/logout')
def logout_admin():
    session['email'] = None
    print("logout")
    # return redirect(url_for('home'))


def delete_employee(employee_id):
    Employee.get_by_employee_id(employee_id).delete()


# @employee_blueprint.route('/showEmployee')
# def showEmployee():
#     Employee.all()
#


def edit_employee(designation, monthly_salary, employee_id):
    employee = Employee.get_by_employee_id(employee_id)

    if designation != "":
        employee.designation = designation
    if monthly_salary != "":
        employee.monthly_salary = monthly_salary

        employee.update_to_db()


def get_employees(company_id):
    employees = Employee.get_by_id(company_id)
    print(employees)
    return employees


def get_by_department_id(department_id):
    employees = Employee.get_by_department_id(department_id)
    return employees
