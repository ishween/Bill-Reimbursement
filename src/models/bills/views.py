from flask import render_template, request, redirect, url_for, Blueprint, session
from src.models.bills.bill import Bill
from src.models.bills.constants import send_email
from src.models.employees.employee import Employee
from src.models.billTypes.billType import BillType
from src.models.managers.manager import Manager
from src.models.department.department import Department
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import src.decorators as bills_decorators

bill_blueprint = Blueprint('bills', __name__)


@bill_blueprint.route('/viewBills/<string:sort_type>/<string:filter_type>', methods=['GET'])
@bills_decorators.requires_login
def view_bills(sort_type, filter_type):
    email = session['email']
    employee = Employee.get_by_employee_email(email)
    filter_bills = None
    if filter_type == "all":
        filter_bills = Bill.all_bills_for_employee(employee['_id'])
    else:
        filter_bills = Bill.all_bills_for_employee_filter(employee['_id'], filter_type)
    sorted_bills = None
    if sort_type != "default":
        sorted_bills = sorted(filter_bills, key=lambda k: k[sort_type])
    else:
        sorted_bills = filter_bills
    return render_template('employees/view_bills.html', bills=sorted_bills, sort_type=sort_type, filter_type=filter_type)


@bill_blueprint.route('/add', methods=['GET', 'POST'])
@bills_decorators.requires_login
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
@bills_decorators.requires_login
def delete_bill(bill_id):
    Bill.delete(bill_id)
    return redirect(url_for('.view_bills', sort_type="default", filter_type="all"))


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
@bills_decorators.requires_login
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
        if bill_type != "":
            bill.bill_type = bill_type
        if url is not None:
            bill.bill_image_url = url

        bill.update_to_db()

    return render_template('employees/edit_bill.html', bill_types=bill_types)


@bill_blueprint.route('/manager/viewBills/<string:sort_type>/<string:filter_type>', methods=['GET'])
@bills_decorators.requires_login
def view_bills_to_manager(sort_type, filter_type):
    email = session['email']
    manager = Manager.get_by_manager_email(email)
    filter_bills = None
    if filter_type == "pending" and filter_type is None:
        filter_bills = Bill.all_bills(manager['department_id'], "pending")
    else:
        filter_bills = Bill.all_bills(manager['department_id'], filter_type)
    response = []
    for bill in filter_bills:
        res={}
        res['_id'] = bill['_id']
        res['bill_type'] = bill['bill_type']
        res['bill_image_url'] = bill['bill_image_url']
        res['date_of_submission'] = bill['date_of_submission']
        res['status'] = bill['status']
        employee_id = bill['employee_id']
        employee = Employee.get_by_employee_id(employee_id)
        res['employee_name'] = employee.name
        res['employee_designation'] = employee.designation
        department = Department.get_by_id(bill['department_id'])
        res['department_name'] = department['name']
        response.append(res)

    sorted_bills = None
    if sort_type == "default":
        sorted_bills = response
    else:
        sorted_bills = sorted(response, key=lambda k: k[sort_type])

    return render_template('managers/view_bills.html', response=sorted_bills, sort_type=sort_type, filter_type=filter_type)


@bill_blueprint.route('/manager/accept/<string:bill_id>', methods=['GET', 'POST'])
@bills_decorators.requires_login
def accept_bill(bill_id):
    bill = Bill.get_by_id(bill_id)
    employee_id = bill.employee_id
    employee_email = Employee.get_by_employee_id(employee_id)
    # if request.method == 'POST':
    reimburse_amount = request.form['reimburse']

    send_email(employee_email.email, reimburse_amount, "accept")

    bill.status = "accept"
    bill.update_to_db()
    bill = Bill.get_by_id(bill_id)
    print(bill)
    return redirect(url_for('.view_bills_to_manager', sort_type="default", filter_type="pending"))


@bill_blueprint.route('/manager/reject/<string:bill_id>', methods=['GET'])
@bills_decorators.requires_login
def reject_bill(bill_id):
    bill = Bill.get_by_id(bill_id)
    employee_id = bill.employee_id
    email = Employee.get_by_employee_id(employee_id)
    send_email(email.email, 0, "reject")

    bill.status = "reject"
    bill.update_to_db()

    return redirect(url_for('.view_bills_to_manager', sort_type="default", filter_type="pending"))
