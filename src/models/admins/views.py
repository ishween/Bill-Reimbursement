from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
import src.models.admins.errors as adminErrors
from src.models.admins.admin import Admin
from src.models.department.views import add_department, view_departments
from src.models.billTypes.views import add_bill_type, delete_bill_type, get_bills_type_by_department
from src.models.managers.views import add_manager, delete_manager, view_managers, get_managers_by_department
from src.models.employees.views import add_an_employee, delete_employee, get_employees, get_by_department_id

__author__ = 'ishween'

admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/login', methods=['GET','POST'])
def login_admin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if Admin.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for('.to_menu'))
        except adminErrors.AdminErrors as a:
            return a.message

    return render_template('admins/login_admin.html')


@admin_blueprint.route('/register', methods=['GET', 'POST'])
def register_admin():
    if request.method == 'POST':
        company_name = request.form['company_name']
        ceo = request.form['ceo']
        email = request.form['email']
        password = request.form['password']
        contact = request.form['contact']
        gst_no = request.form['gst_no']

        try:
            if Admin.register(company_name, ceo, email, password, contact, gst_no):
                session['email'] = email
                return redirect(url_for('.to_menu'))
        except adminErrors.AdminErrors as a:
            return a.message

    return render_template('admins/register.html')


@admin_blueprint.route('/logout')
def logout_admin():
    session['email'] = None
    return redirect(url_for('home'))


@admin_blueprint.route('/viewDepartments', methods=['GET'])
def view_departments_admin():
    print("calling")
    company_id = Admin.get_by_email(session['email'])
    departments = view_departments(company_id)
    return render_template('department/show_departments.html', departments=departments)


@admin_blueprint.route('/admin', methods=['GET'])
def to_menu():
    return render_template('admin_menue.html')


@admin_blueprint.route('/addDepartment', methods=['GET', 'POST'])
def add_a_department():
    if request.method == 'POST':
        company_id = Admin.get_by_email(session['email'])
        name = request.form['name']

        add_department(company_id, name)
    return render_template('department/add_department.html')


@admin_blueprint.route('/viewBillTypes', methods=['GET'])
def view_bill_types_admin():
    company_id = Admin.get_by_email(session['email'])
    departments = view_departments(company_id)
    response = []
    for department in departments:
        res={}
        res['department_id'] = department['_id']
        res['department_name'] = department['name']
        res['bills_type'] = []
        bills_type = get_bills_type_by_department(department['_id'])
        for billtype in bills_type:
            res['bills_type'].append(billtype)
        response.append(res)
    return render_template('bill_types/show_bills.html', response=response)


@admin_blueprint.route('/addBillType', methods=['GET', 'POST'])
def add_a_bill_type():
    company_id = Admin.get_by_email(session['email'])
    departments = view_departments(company_id)
    if request.method == 'POST':
        department_id = request.form['department_id']
        type = request.form['type']
        reimbursement = request.form['reimbursement']

        add_bill_type(department_id, type, reimbursement)

    return render_template('bill_types/add_bill.html', departments=departments)


@admin_blueprint.route('/viewManagers', methods=['GET'])
def view_managers_admin():
    company_id = Admin.get_by_email(session['email'])
    #managers = view_managers(company_id)
    departments = view_departments(company_id)
    response = []
    for department in departments:
        res={}
        dept = department['_id']
        res['department_id'] = dept
        res['department_name'] = department['name']
        res['managers'] = []
        print(dept)
        managers = get_managers_by_department(dept)
        for manager in managers:
            res['managers'].append(manager)
        response.append(res)
    return render_template('managers/show_managers.html', response=response)


@admin_blueprint.route('/addManager', methods=['GET', 'POST'])
def add_a_manager():
    company_id = Admin.get_by_email(session['email'])
    departments = view_departments(company_id)

    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        designation = request.form['designation']
        department_id = request.form['department_id']
        date_of_joining = request.form['date_of_joining']

        add_manager(company_id, email, name, designation, department_id, date_of_joining)

    return render_template('managers/add_manager.html', departments=departments)


@admin_blueprint.route('/viewEmployees', methods=['GET'])
def view_employees_admin():
    company_id = Admin.get_by_email(session['email'])
    departments = view_departments(company_id)
    response = []
    for department in departments:
        res={}
        res['department_id'] = department['_id']
        res['department_name'] = department['name']
        res['employees'] = []
        employees = get_by_department_id(department['_id'])
        for employee in employees:
            if employee['department_id'] == department['_id']:
                res['employees'].append(employee)
        response.append(res)
    return render_template('employees/show_employees.html', response=response)


@admin_blueprint.route('/addEmployee', methods=['GET', 'POST'])
def add_employee():
    company_id = Admin.get_by_email(session['email'])
    departments = view_departments(company_id)

    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        designation = request.form['designation']
        department_id = request.form['department_id']
        date_of_joining = request.form['date_of_joining']
        monthly_salary = request.form['monthly_salary']

        add_an_employee(company_id, email, name, designation, department_id, date_of_joining, monthly_salary)

    return render_template('employees/add_employee.html', departments=departments)


@admin_blueprint.route('/deleteEmployee/<string:employee_id>', methods=['GET'])
def delete_employee(employee_id):
    delete_employee(employee_id)


@admin_blueprint.route('/deleteBillType/<string:bill_type_id>', methods=['GET'])
def delete_bill_type(bill_type_id):
    delete_bill_type(bill_type_id)


@admin_blueprint.route('/deleteManager/<string:manager_id>', methods=['GET'])
def delete_manager(manager_id):
    delete_manager(manager_id)

