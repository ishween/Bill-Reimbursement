from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
import src.models.directors.errors as director_errors
from src.models.directors.director import Director
import src.decorators as director_decorators
from src.db.utils import Utils
from src.models.admins.views import get_by_email_company_id
from src.models.department.views import view_departments, get_department

__author__ = 'ishween'

director_blueprint = Blueprint('director', __name__)


@director_blueprint.route('/login', methods = ['GET','POST'])
def login_director():
    # Login director by accessing email and password entered by the user
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if Director.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for('bills.view_bills_to_director', sort_type="default", filter_type="pending"))
        except director_errors.DirectorError as a:
            return a.message

    return render_template('directors/login_director.html')


@director_blueprint.route('/director/reset', methods = ['GET', 'POST'])
def reset_password():
    # reset old password
    if request.method == 'POST':
        email = session['email']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        try:
            director = Director.is_reset_password_valid(email, old_password)
            director.password = Utils.hash_password(new_password)
            director.update_to_db()
            return redirect(url_for('bills.view_bills_to_director', sort_type="default", filter_type="pending"))
        except director_errors.IncorrectPasswordError as error:
            return error.message

    return render_template('directors/reset_password.html')


@director_blueprint.route('/viewDirectors/<string:sort_type>/<string:filter_type>', methods=['GET'])
@director_decorators.requires_login
def view_directors_admin(sort_type, filter_type):
    # Displays directors of the company to the admin
    company_id = get_by_email_company_id()
    departments = view_departments(company_id)
    response = []
    directors_response = []
    department_response = []

    for department in departments:
        department_response.append(department)

    if filter_type.startswith("department"):
        department_id = filter_type[10:]
        # directors = get_directors_by_department(department_id)
        directors = Director.get_by_department_id(department_id)
        department = get_department(department_id)
        res = {}
        res['department_id'] = department_id
        res['department_name'] = department['name']
        res['directors'] = []
        append_director = []
        for director in directors:
            print(director)
            append_director.append(director)

        if sort_type != "default":
            res['directors'] = sorted(append_director, key=lambda k: k[sort_type])
        else:
            res['directors'] = append_director
        response.append(res)
    else:
        for department in department_response:
            res={}
            dept = department['_id']
            res['department_id'] = dept
            res['department_name'] = department['name']
            res['directors'] = []
            append_director = []
            # directors = get_directors_by_department(dept)
            directors = Director.get_by_department_id(dept)

            for director in directors:
                if filter_type != "default" and filter_type == director['name']:
                    append_director.append(director)
                elif filter_type == "default":
                    append_director.append(director)
                if director['name'] not in directors_response:
                    directors_response.append(director['name'])

            if sort_type != "default":
                res['directors'] = sorted(append_director, key=lambda k: k[sort_type])
            else:
                res['directors'] = append_director
            response.append(res)

    response = sorted(response, key=lambda k: k['department_name'])
    return render_template('admins/show_directors.html', response=response, department_response=department_response, directors_response=directors_response, sort_type=sort_type, filter_type=filter_type)


@director_blueprint.route('/addDirector', methods=['GET', 'POST'])
@director_decorators.requires_login
def add_a_director():
    # Admin add a director of the company
    company_id = get_by_email_company_id()
    departments = view_departments(company_id)

    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        designation = request.form['designation']
        department_id = request.form['department_id']
        date_of_joining = request.form['date_of_joining']

        Director.add_a_director(company_id, email, name, designation, department_id, date_of_joining)

    return render_template('admins/add_director.html', departments=departments)


@director_blueprint.route('/editDirector/<string:director_id>', methods = ['GET', 'POST'])
@director_decorators.requires_login
def admin_edit_director(director_id):
    # Admin edits a director
    if request.method == 'POST':
        designation = request.form['designation']

        # edit_director(designation, director_id)
        director = Director.get_by_director_id(director_id)
        if designation != "":
            director.designation = designation
            director.update_to_db()
        return redirect(url_for('director.view_directors_admin', sort_type="default", filter_type="default"))
    return render_template('admins/edit_director.html')


@director_blueprint.route('/deleteDirector/<string:director_id>', methods=['GET'])
@director_decorators.requires_login
def admin_delete_director(director_id):
    # Admin delete a director of the company
    delete_director(director_id)
    return redirect(url_for('director.view_directors_admin', sort_type="default", filter_type="default"))


def delete_director(director_id):
    Director.get_by_director_id(director_id).delete()


@director_blueprint.route('/director/logout')
def logout_admin():
    # Director logout from the session
    session['email'] = None
    print("logout")
    #return redirect(url_for('home'))
