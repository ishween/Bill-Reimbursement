from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
import src.models.managers.error as managerErrors
from src.models.managers.manager import Manager
import src.decorators as manager_decorators
from src.db.utils import Utils
from src.models.admins.views import get_by_email_company_id
from src.models.department.views import view_departments, get_department

__author__ = 'ishween'

manager_blueprint = Blueprint('manager', __name__)


@manager_blueprint.route('/manager/login', methods = ['GET','POST'])
def login_manager():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if Manager.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for('manager.to_menu', sort_type="default", filter_type="pending"))
        except managerErrors.ManagerError as a:
            return a.message

    return render_template('managers/login_manager.html')


@manager_blueprint.route('/manager', methods=['GET'])
def to_menu():
    return render_template('managers/manager_menu.html')

@manager_blueprint.route('/viewManagers/<string:sort_type>/<string:filter_type>', methods=['GET'])
@manager_decorators.requires_login
def view_managers_admin(sort_type, filter_type):
    company_id = get_by_email_company_id()
    #managers = view_managers(company_id)
    departments = view_departments(company_id)
    response = []
    managers_response = []
    department_response = []

    for department in departments:
        department_response.append(department)

    if filter_type.startswith("department"):
        department_id = filter_type[10:]
        # managers = get_managers_by_department(department_id)
        managers = Manager.get_by_department_id(department_id)
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
            # managers = get_managers_by_department(dept)
            managers = Manager.get_by_department_id(dept)

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


@manager_blueprint.route('/addManager', methods=['GET', 'POST'])
@manager_decorators.requires_login
def add_a_manager():
    company_id = get_by_email_company_id()
    departments = view_departments(company_id)

    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        designation = request.form['designation']
        department_id = request.form['department_id']
        date_of_joining = request.form['date_of_joining']

        # add_manager(company_id, email, name, designation, department_id, date_of_joining)
        Manager.add_a_manager(company_id, email, name, designation, department_id, date_of_joining)

    return render_template('admins/add_manager.html', departments=departments)


@manager_blueprint.route('/editManager/<string:manager_id>', methods = ['GET', 'POST'])
@manager_decorators.requires_login
def admin_edit_manager(manager_id):
    if request.method == 'POST':
        designation = request.form['designation']

        # edit_manager(designation, manager_id)
        manager = Manager.get_by_manager_id(manager_id)
        if designation != "":
            manager.designation = designation
            manager.update_to_db()
        return redirect(url_for('manager.view_managers_admin', sort_type="default", filter_type="default"))
    return render_template('admins/edit_manager.html')


@manager_blueprint.route('/deleteManager/<string:manager_id>', methods=['GET'])
@manager_decorators.requires_login
def admin_delete_manager(manager_id):
    # delete_manager(manager_id)
    Manager.get_by_manager_id(manager_id).delete()
    return redirect(url_for('manager.view_managers_admin', sort_type="default", filter_type="default"))


@manager_blueprint.route('/manager/logout')
def logout_admin():
    session['email'] = None
    print("logout")
    #return redirect(url_for('home'))


@manager_blueprint.route('/manager/reset', methods = ['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = session['email']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        try:
            employee = Manager.is_reset_password_valid(email, old_password)
            employee.password = Utils.hash_password(new_password)
            employee.update_to_db()
            return redirect(url_for('manager.to_menu', sort_type="default", filter_type="pending"))
        except managerErrors.IncorrectPasswordError as error:
            return error.message

    return render_template('managers/reset_password.html')
