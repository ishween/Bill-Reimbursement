from flask import render_template, request, redirect, url_for, Blueprint
from src.models.bills.bill import Bill
from src.models.bills.constants import send_email
from src.models.employees.employee import Employee

bill_blueprint = Blueprint('bills', __name__)

#
# @bill_blueprint.route('/')
# def index():
#     Bill.all()


def show_bills(department_id, status):
    Bill.all_bills(department_id, status)

#@bill_blueprint.route('/add', methods = ['GET', 'POST'])
def add_bill(employee_id, bill_type, department_id, date_of_submission, bill_image):
    # if request.method == 'POST':
    #     employee_id = request.form['employee_id']
    #     bill_type = request.form['bill_type']
    #     department = request.form['department']
    #     date_of_submission = request.form['date_of_submission']
    #     bill_image = request.form['bill_image']

    Bill.add_bill(employee_id, bill_type, department_id, date_of_submission, bill_image)


#@bill_blueprint.route('/delete/<string:bill_id>', methods = ['GET'])
def delete_bill(bill_id):
    Bill.get_by_id(bill_id).delete()
    #redirect(url_for('.index'))


#@bill_blueprint.route('/edit/<string:bill_id>', methods=['GET', 'POST'])
def change_status(bill_id, status):
    bill = Bill.get_by_id(bill_id)

    bill.status = status

    bill.save_to_db()
    email = Employee.get_by_id(bill.employee_id)
    send_email(email, status)
    #return redirect(url_for('.index'))

    #return render_template('stores/edit_store.html', store=store)


def edit_bill(bill_id, bill_type, bill_image):
    bill = Bill.get_by_id(bill_id)

    bill.bill_type = bill_type
    bill.bill_image = bill_image

    bill.save_to_db()