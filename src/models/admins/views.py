from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
import src.models.admins.errors as admin_errors
from src.models.admins.admin import Admin
import src.decorators as admin_decorators
from src.db.utils import Utils

__author__ = 'ishween'

admin_blueprint = Blueprint('admin', __name__)


def get_by_email_company_id():
    # to get company ID using admin email
    print(Admin.get_by_email(session['email']))
    return Admin.get_by_email(session['email'])


@admin_blueprint.route('/login', methods=['GET','POST'])
def login_admin():
    # Login admin by accessing email and password entered by the user
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if Admin.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for('.to_menu'))
        except admin_errors.AdminErrors as a:
            return a.message

    return render_template('admins/login_admin.html')


@admin_blueprint.route('/register', methods=['GET', 'POST'])
def register_admin():
    # register company and admin that will handle company updates
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
        except admin_errors.AdminErrors as a:
            return a.message

    return render_template('admins/register.html')


@admin_blueprint.route('/menu', methods=['GET'])
@admin_decorators.requires_login
def to_menu():
    # to display admin menu
    return render_template('admins/admin_menu.html')


@admin_blueprint.route('/reset', methods = ['GET', 'POST'])
def reset_password():
    # reset old password
    if request.method == 'POST':
        email = session['email']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        try:
            admin = Admin.is_reset_password_valid(email, old_password)
            admin.password = Utils.hash_password(new_password)
            admin.update_to_db()
            return redirect(url_for('.to_menue', sort_type="default", filter_type="pending"))
        except admin_errors.IncorrectPasswordError as error:
            return error.message

    return render_template('admins/reset_password.html')


@admin_blueprint.route('/logout')
def logout_admin():
    # to logout from session
    session['email'] = None
    return redirect(url_for('home'))
