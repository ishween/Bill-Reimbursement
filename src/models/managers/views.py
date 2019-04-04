from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
import src.models.managers.error as managerErrors
from src.models.managers.manager import Manager
from src.models.bills.views import change_status
import src.decorators as manager_decorators

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
                return redirect(url_for('bills.view_bills_to_manager', sort_type="default", filter_type="pending"))
        except managerErrors.ManagerError as a:
            return a.message

    return render_template('managers/login_manager.html')


@manager_blueprint.route('/manager', methods=['GET'])
def to_menu():
    return render_template('managers/manager_menu.html')


def add_manager(company_id, email, name, designation, department_id, date_of_joining):
    Manager.add_a_manager(company_id, email, name, designation, department_id, date_of_joining)


# @manager_blueprint.route('/show_all_bills/<string:department_id>/<string:status>', methods = ['GET'])
# def show_all_bills(department_id, status):
#     show_bills(department_id, status)


def edit_manager(designation, manager_id):
    manager = Manager.get_by_manager_id(manager_id)
    if designation != "":
        manager.designation = designation
        manager.update_to_db()
        return redirect(url_for('admin.view_managers_admin', sort_type="default", filter_type="default"))
    return render_template('admins/edit_manager.html')


def delete_manager(manager_id):
    Manager.get_by_manager_id(manager_id).delete()

@manager_blueprint.route('/manager/logout')
def logout_admin():
    session['email'] = None
    print("logout")
    #return redirect(url_for('home'))

@manager_blueprint.route('/status/<string:bill_id>/<string:status>', methods = ['POST'])
@manager_decorators.requires_login
def change_status(bill_id, status):
    change_status(bill_id, status)


def view_managers(company_id):
    managers = Manager.get_by_id(company_id)
    # for man in managers:
    #     print(man._id)
    #print(managers)
    return managers


def get_managers_by_department(department_id):
    managers = Manager.get_by_department_id(department_id)
    return managers
