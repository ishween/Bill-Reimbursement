from flask import render_template, request, redirect, url_for, Blueprint, session
from src.models.bills.bill import Bill
from src.models.bills.constants import send_email
from src.models.employees.employee import Employee
from src.models.billTypes.billType import BillType
from src.models.managers.manager import Manager
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

bill_blueprint = Blueprint('bills', __name__)

#
# @bill_blueprint.route('/')
# def index():
#     Bill.all()


@bill_blueprint.route('/viewBills', methods=['GET'])
def view_bills():
    email = session['email']
    employee = Employee.get_by_employee_email(email)
    bills = Bill.all_bills_for_employee(employee['_id'])
    print(bills)
    return render_template('employees/view_bills.html', bills=bills)


@bill_blueprint.route('/add', methods=['GET', 'POST'])
def add_bill():
    employee_email = session['email']
    employee = Employee.get_by_employee_email(employee_email)
    employee_id = employee['_id']
    employee_name = employee['name']
    department_id = employee['department_id']
    bill_types = BillType.all_bills_type_by_department_id(department_id)
    url = None
    thumbnail_url1 = None
    upload_result = None
    if request.method == 'POST':
        bill_type = request.form['type']
        date_of_submission = request.form['date_of_submission']
        file_to_upload = request.files['file']
        if file_to_upload:
            upload_result = upload(file_to_upload)
            url = upload_result['url']
            thumbnail_url1, options = cloudinary_url(upload_result['public_id'], format="png", crop="fill", width=100,
                                                     height=100)
        bill_image_url = url

        Bill.add_bill(employee_id, bill_type, department_id, date_of_submission, bill_image_url)

    return render_template('employees/add_bill.html', upload_result=upload_result, url=url, thumbnail_url1=thumbnail_url1, bill_types=bill_types,
                           employee_name=employee_name, department_id=department_id)


@bill_blueprint.route('/delete/<string:bill_id>', methods=['GET'])
def delete_bill(bill_id):
    Bill.delete(bill_id)
    return redirect(url_for('.view_bills'))


#@bill_blueprint.route('/edit/<string:bill_id>', methods=['GET', 'POST'])
def change_status(bill_id, status):
    bill = Bill.get_by_id(bill_id)

    bill.status = status

    bill.save_to_db()
    email = Employee.get_by_id(bill.employee_id)
    send_email(email, status)
    #return redirect(url_for('.index'))

    #return render_template('stores/edit_store.html', store=store)


@bill_blueprint.route('/editBill/<string:bill_id>', methods=['GET', 'POST'])
def edit_bill(bill_id):
    bill = Bill.get_by_id(bill_id)
    employee_email = session['email']
    employee = Employee.get_by_employee_email(employee_email)
    department_id = employee['department_id']
    bill_types = BillType.all_bills_type_by_department_id(department_id)
    url = None
    thumbnail_url1 = None
    if request.method == 'POST':
        bill_type = request.form['type']
        file_to_upload = request.files['file']
        if file_to_upload:
            upload_result = upload(file_to_upload)
            url = upload_result['url']
            # thumbnail_url1, options = cloudinary_url(upload_result['public_id'], format="png", crop="fill", width=100,
            #                                          height=100)
        if bill_type != "":
            bill.bill_type = bill_type
        if url is not None:
            bill.bill_image_url = url

        bill.update_to_db()

    return render_template('employees/edit_bill.html', bill_types=bill_types)


@bill_blueprint.route('/manager/viewBills', methods=['GET'])
def view_bills_to_manager():
    email = session['email']
    manager = Manager.get_by_manager_email(email)
    bills = Bill.all_bills(manager['department_id'], "pending")
    return render_template('managers/view_bills.html', bills=bills)


@bill_blueprint.route('/manager/accept/<string:bill_id>', methods=['GET', 'POST'])
def accept_bill(bill_id):
    bill = Bill.get_by_id(bill_id)
    employee_id = bill.employee_id
    employee_email = Employee.get_by_employee_id(employee_id)
    # if request.method == 'POST':
    print("yes")
    reimburse_amount = request.form['reimburse']

    send_email(employee_email.email, reimburse_amount, "accept")

    bill.status = "accept"
    bill.update_to_db()
    bill = Bill.get_by_id(bill_id)
    print(bill)
    return redirect(url_for('.view_bills_to_manager'))


@bill_blueprint.route('/manager/reject/<string:bill_id>', methods=['GET'])
def reject_bill(bill_id):
    bill = Bill.get_by_id(bill_id)
    employee_id = bill.employee_id
    email = Employee.get_by_employee_id(employee_id)
    send_email(email.email, 0, "reject")

    bill.status = "reject"
    bill.update_to_db()

    return redirect(url_for('.view_bills_to_manager'))
