from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
import src.models.directors.errors as directorErrors
from src.models.directors.director import Director
import src.decorators as director_decorators
from src.db.utils import Utils

__author__ = 'ishween'

director_blueprint = Blueprint('director', __name__)


@director_blueprint.route('/login', methods = ['GET','POST'])
def login_director():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if Director.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for('bills.view_bills_to_director', sort_type="default", filter_type="pending"))
        except directorErrors.DirectorError as a:
            return a.message

    return render_template('directors/login_director.html')


@director_blueprint.route('/director/reset', methods = ['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = session['email']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        try:
            director = Director.is_reset_password_valid(email, old_password)
            director.password = Utils.hash_password(new_password)
            director.update_to_db()
            return redirect(url_for('bills.view_bills_to_director', sort_type="default", filter_type="pending"))
        except directorErrors.IncorrectPasswordError as error:
            return error.message

    return render_template('directors/reset_password.html')

def add_director(company_id, email, name, designation, department_id, date_of_joining):
    Director.add_a_director(company_id, email, name, designation, department_id, date_of_joining)


def edit_director(designation, director_id):
    director = Director.get_by_director_id(director_id)
    if designation != "":
        director.designation = designation
        director.update_to_db()
        # return redirect(url_for('admin.view_directors_admin', sort_type="default", filter_type="default"))
    # return render_template('admins/edit_director.html')


def delete_director(director_id):
    Director.get_by_director_id(director_id).delete()


@director_blueprint.route('/director/logout')
def logout_admin():
    session['email'] = None
    print("logout")
    #return redirect(url_for('home'))


def view_director(company_id):
    directors = Director.get_by_id(company_id)
    return Director


def get_directors_by_department(department_id):
    directors = Director.get_by_department_id(department_id)
    return directors