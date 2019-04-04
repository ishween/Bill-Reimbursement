from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
import src.models.admins.errors as adminErrors
from src.models.admins.admin import Admin
from src.models.department.views import add_department, view_departments, get_department
from src.models.billTypes.views import add_bill_type, delete_bill_type, get_bills_type_by_department
from src.models.managers.views import add_manager, delete_manager, view_managers, get_managers_by_department
from src.models.employees.views import add_an_employee, delete_employee, get_employees, get_by_department_id, edit_employee
import src.decorators as admin_decorators

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
@admin_decorators.requires_login
def view_departments_admin():
    print("calling")
    company_id = Admin.get_by_email(session['email'])
    departments = view_departments(company_id)
    return render_template('admins/show_departments.html', departments=departments)


@admin_blueprint.route('/admin', methods=['GET'])
@admin_decorators.requires_login
def to_menu():
    return render_template('admin_menue.html')


@admin_blueprint.route('/addDepartment', methods=['GET', 'POST'])
@admin_decorators.requires_login
def add_a_department():
    if request.method == 'POST':
        company_id = Admin.get_by_email(session['email'])
        name = request.form['name']

        add_department(company_id, name)
    return render_template('admins/add_department.html')


@admin_blueprint.route('/viewBillTypes/<string:sort_type>/<string:filter_type>', methods=['GET'])
@admin_decorators.requires_login
def view_bill_types_admin(sort_type, filter_type):
    company_id = Admin.get_by_email(session['email'])
    departments = view_departments(company_id)
    response = []
    types = []
    department_response = []

    for department in departments:
        department_response.append(department)

    if filter_type.startswith("department"):
        department_id = filter_type[10:]
        bills_type = get_bills_type_by_department(department_id)
        department = get_department(department_id)
        res = {}
        res['department_id'] = department_id
        res['department_name'] = department['name']
        res['bills_type'] = []
        billtypes = []

        for billtype in bills_type:
            billtypes.append(billtype)
            if billtype['type'] not in types:
                types.append(billtype['type'])

        if sort_type != "default":
            res['bills_type'] = sorted(billtypes, key=lambda k: k[sort_type])
        else:
            res['bills_type'] = billtypes
        response.append(res)
    else:
        for department in department_response:
            res={}
            res['department_id'] = department['_id']
            res['department_name'] = department['name']
            res['bills_type'] = []
            billtypes = []

            bills_type = get_bills_type_by_department(department['_id'])

            for billtype in bills_type:
                if filter_type != "default" and filter_type == billtype['type']:
                    billtypes.append(billtype)
                elif filter_type == "default":
                    billtypes.append(billtype)
                if billtype['type'] not in types:
                    types.append(billtype['type'])

            if sort_type != "default":
                res['bills_type'] = sorted(billtypes, key=lambda k: k[sort_type])
            else:
                res['bills_type'] = billtypes
            response.append(res)

    response = sorted(response, key=lambda k: k['department_name']) #alphabetical order

    return render_template('admins/show_bill_types.html', response=response, department_response=department_response, types=types, sort_type=sort_type, filter_type=filter_type)


@admin_blueprint.route('/addBillType', methods=['GET', 'POST'])
@admin_decorators.requires_login
def add_a_bill_type():
    company_id = Admin.get_by_email(session['email'])
    departments = view_departments(company_id)
    if request.method == 'POST':
        department_id = request.form['department_id']
        type = request.form['type']
        reimbursement = request.form['reimbursement']

        add_bill_type(department_id, type, reimbursement)

    return render_template('admins/add_bill_type.html', departments=departments)


@admin_blueprint.route('/viewManagers/<string:sort_type>/<string:filter_type>', methods=['GET'])
@admin_decorators.requires_login
def view_managers_admin(sort_type, filter_type):
    company_id = Admin.get_by_email(session['email'])
    #managers = view_managers(company_id)
    departments = view_departments(company_id)
    response = []
    managers_response = []
    department_response = []

    for department in departments:
        department_response.append(department)

    if filter_type.startswith("department"):
        department_id = filter_type[10:]
        managers = get_managers_by_department(department_id)
        department = get_department(department_id)
        res = {}
        res['department_id'] = department_id
        res['department_name'] = department['name']
        res['managers'] = []
        append_managers = []
        for manager in managers:
            append_managers.append(manager)

        if sort_type != "default":
            res['managers'] = sorted(append_managers, key=lambda k: k[sort_type])
        else:
            res['managers'] = append_managers
        response.append(res)
    else:
        for department in department_response:
            res={}
            dept = department['_id']
            res['department_id'] = dept
            res['department_name'] = department['name']
            res['managers'] = []
            append_managers = []
            managers = get_managers_by_department(dept)

            for manager in managers:
                if filter_type != "default" and filter_type == manager['name']:
                    append_managers.append(manager)
                elif filter_type == "default":
                    append_managers.append(manager)
                if manager['name'] not in managers_response:
                    managers_response.append(manager['name'])

            if sort_type != "default":
                res['managers'] = sorted(append_managers, key=lambda k: k[sort_type])
            else:
                res['managers'] = append_managers
            response.append(res)

    response = sorted(response, key=lambda k: k['department_name'])
    return render_template('admins/show_managers.html', response=response, department_response=department_response, managers_response=managers_response, sort_type=sort_type, filter_type=filter_type)


@admin_blueprint.route('/addManager', methods=['GET', 'POST'])
@admin_decorators.requires_login
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

    return render_template('admins/add_manager.html', departments=departments)


@admin_blueprint.route('/viewEmployees/<string:sort_type>/<string:filter_type>', methods=['GET'])
@admin_decorators.requires_login
def view_employees_admin(sort_type, filter_type):
    company_id = Admin.get_by_email(session['email'])
    departments = view_departments(company_id)
    response = []
    department_response = []
    for department in departments:
        department_response.append(department)

    if filter_type.startswith("department"):
        department_id = filter_type[10:]
        employees = get_by_department_id(department_id)
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

            employees = get_by_department_id(department['_id'])
            for employee in employees:
                append_employees.append(employee)

            if sort_type != "default":
                res['employees'] = sorted(append_employees, key=lambda k: k[sort_type])
            else:
                res['employees'] = append_employees

            response.append(res)

    response = sorted(response, key=lambda k: k['department_name'])
    return render_template('admins/show_employees.html', response=response, department_response=department_response, sort_type=sort_type, filter_type=filter_type)


@admin_blueprint.route('/addEmployee', methods=['GET', 'POST'])
@admin_decorators.requires_login
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

    return render_template('admins/add_employee.html', departments=departments)


@admin_blueprint.route('/edit/<string:employee_id>', methods=['GET', 'POST'])
@admin_decorators.requires_login
def admin_edit_employee(employee_id):
    if request.method == 'POST':
        designation = request.form['designation']
        monthly_salary = request.form['monthly_salary']

        print(type(designation))
        print(type(monthly_salary))

        edit_employee(designation, monthly_salary, employee_id)
        return redirect(url_for('admin.view_employees_admin', sort_type="default", filter_type="default"))
    return render_template('admins/edit_employee.html')


@admin_blueprint.route('/deleteEmployee/<string:employee_id>', methods=['GET'])
@admin_decorators.requires_login
def admin_delete_employee(employee_id):
    delete_employee(employee_id)
    return redirect(url_for('admin.view_employees_admin', sort_type="default", filter_type="default"))


@admin_blueprint.route('/deleteBillType/<string:bill_type_id>', methods=['GET'])
@admin_decorators.requires_login
def delete_bill_type(bill_type_id):
    delete_bill_type(bill_type_id)


@admin_blueprint.route('/deleteManager/<string:manager_id>', methods=['GET'])
@admin_decorators.requires_login
def delete_manager(manager_id):
    delete_manager(manager_id)

