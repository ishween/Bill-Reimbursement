from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
import src.models.managers.error as managerErrors
from src.models.managers.manager import Manager
from src.models.bills.views import show_bills, change_status

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
                #return redirect(url_for('.user_alerts'))
                print("login")
        except managerErrors.ManagerError as a:
            return a.message

    #return  render_template('users/login.html')


#@manager_blueprint.route('/admin/addManager', methods = ['GET', 'POST'])
#def add_employee():
#    if request.method == 'POST':
#         company_id = request.form['company_id']
#         email = request.form['email']
#         name = request.form['name']
#         designation = request.form['designation']
#         department_id = request.form['department_id']
#         date_of_joining = request.form['date_of_joining']
#
#         Manager.add_a_manager(company_id, email, name, designation, department_id, date_of_joining)
#     return  render_template('users/login.html')

def add_manager(company_id, email, name, designation, department_id, date_of_joining):
    Manager.add_a_manager(company_id, email, name, designation, department_id, date_of_joining)


@manager_blueprint.route('/show_all_bills/<string:department_id>/<string:status>', methods = ['GET'])
def show_all_bills(department_id, status):
    show_bills(department_id, status)


@manager_blueprint.route('/editManager/<string:manager_id>', methods = ['GET', 'POST'])
def edit_manager(manager_id):
    manager = Manager.get_by_manager_id(manager_id)
    if request.method == 'POST':
        designation = request.form['designation']

        manager.designation = designation

        manager.update_to_db()
        return redirect(url_for('admin.view_managers_admin'))
    return render_template('managers/edit_manager.html')


@manager_blueprint.route('/deleteManager/<string:manager_id>', methods = ['GET'])
def delete_manager(manager_id):
    Manager.get_by_manager_id(manager_id).delete()
    return redirect(url_for('admin.view_managers_admin'))

@manager_blueprint.route('/manager/logout')
def logout_admin():
    session['email'] = None
    print("logout")
    #return redirect(url_for('home'))

@manager_blueprint.route('/status/<string:bill_id>/<string:status>', methods = ['POST'])
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
