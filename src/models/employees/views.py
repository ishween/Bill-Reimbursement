from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
import src.models.employees.error as employee_errors
from src.models.employees.employee import Employee
from src.db.utils import Utils
import src.decorators as employee_decorators
from src.models.admins.views import get_by_email_company_id
from src.models.department.views import view_departments, get_department

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
        except employee_errors.EmployeeError as a:
            return a.message

    return render_template('employees/login_employee.html')


@employee_blueprint.route('/employee/reset', methods = ['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = session['email']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        try:
            employee = Employee.is_reset_password_valid(email, old_password)
            employee.password = Utils.hash_password(new_password)
            employee.update_to_db()
            return redirect(url_for('bills.view_bills', sort_type="default", filter_type="all"))
        except employee_errors.IncorrectPasswordError as error:
            return error.message

    return render_template('employees/reset_password.html')


@employee_blueprint.route('/employee', methods=['GET'])
def to_menu():
    return render_template('employees/view_bills.html')


@employee_blueprint.route('/employee/logout')
def logout_admin():
    session['email'] = None
    print("logout")
    # return redirect(url_for('home'))

@employee_blueprint.route('/viewEmployees/<string:sort_type>/<string:filter_type>', methods=['GET'])
@employee_decorators.requires_login
def view_employees_admin(sort_type, filter_type):
    company_id = get_by_email_company_id()
    departments = view_departments(company_id)
    response = []
    department_response = []
    for department in departments:
        department_response.append(department)

    if filter_type.startswith("department"):
        department_id = filter_type[10:]
        # employees = get_by_department_id(department_id)
        employees = Employee.get_by_department_id(department_id)
        department = get_department(department_id)
        res={}
        res['department_id'] = department_id
        res['department_name'] = department['name']
        res['employees'] = []
        append_employees = []

        for employee in employees:
            append_employees.append(employee)

        if sort_type != "default":
            res['employees'] = sorted(append_employees, key=lambda k: k[sort_type])
        else:
            res['employees'] = append_employees
        response.append(res)
    else:
        # for department in departments:
        #     print(department) - I am unable to use departments again for iterating why so in python?
        for department in department_response:
            res={}
            res['department_id'] = department['_id']
            res['department_name'] = department['name']
            res['employees'] = []
            append_employees = []

            # employees = get_by_department_id(department['_id'])
            employees = Employee.get_by_department_id(department['_id'])
            for employee in employees:
                append_employees.append(employee)

            if sort_type != "default":
                res['employees'] = sorted(append_employees, key=lambda k: k[sort_type])
            else:
                res['employees'] = append_employees

            response.append(res)

    response = sorted(response, key=lambda k: k['department_name'])
    return render_template('admins/show_employees.html', response=response, department_response=department_response, sort_type=sort_type, filter_type=filter_type)


@employee_blueprint.route('/addEmployee', methods=['GET', 'POST'])
@employee_decorators.requires_login
def add_employee():
    company_id = get_by_email_company_id()
    departments = view_departments(company_id)

    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        designation = request.form['designation']
        department_id = request.form['department_id']
        date_of_joining = request.form['date_of_joining']
        monthly_salary = request.form['monthly_salary']

        Employee.add_an_employee(company_id, email, name, designation, department_id, date_of_joining, monthly_salary)

    return render_template('admins/add_employee.html', departments=departments)


@employee_blueprint.route('/edit/<string:employee_id>', methods=['GET', 'POST'])
@employee_decorators.requires_login
def admin_edit_employee(employee_id):
    if request.method == 'POST':
        designation = request.form['designation']
        monthly_salary = request.form['monthly_salary']

        print(type(designation))
        print(type(monthly_salary))

        # edit_employee(designation, monthly_salary, employee_id)
        employee = Employee.get_by_employee_id(employee_id)

        if designation != "":
            employee.designation = designation
        if monthly_salary != "":
            employee.monthly_salary = monthly_salary

        employee.update_to_db()
        return redirect(url_for('employees.view_employees_admin', sort_type="default", filter_type="default"))
    return render_template('admins/edit_employee.html')


@employee_blueprint.route('/deleteEmployee/<string:employee_id>', methods=['GET'])
@employee_decorators.requires_login
def admin_delete_employee(employee_id):
    # delete_employee(employee_id)
    Employee.get_by_employee_id(employee_id).delete()
    return redirect(url_for('employees.view_employees_admin', sort_type="default", filter_type="default"))
