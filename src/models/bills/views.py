from flask import render_template, request, redirect, url_for, Blueprint, session
from src.models.bills.bill import Bill
from src.models.bills.constants import send_email
from src.models.employees.employee import Employee
from src.models.billTypes.billType import BillType
from src.models.billTypes.views import get_bill_amount_by_department_and_type
from src.models.managers.manager import Manager
from src.models.directors.director import Director
from src.models.department.department import Department
import src.models.bills.error as BillErrors
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import src.decorators as bills_decorators
import matplotlib.pyplot as plt
import pandas as pd


bill_blueprint = Blueprint('bills', __name__)


@bill_blueprint.route('/viewBills/<string:sort_type>/<string:filter_type>', methods=['GET'])
@bills_decorators.requires_login
def view_bills(sort_type, filter_type):
    email = session['email']
    employee = Employee.get_by_employee_email(email)
    filter_bills = None
    if filter_type == "all" or filter_type == 'None':
        filter_bills = Bill.all_bills_for_employee(employee['_id'])
    else:
        filter_bills = Bill.all_bills_for_employee_filter(employee['_id'], filter_type)
    sorted_bills = None
    if sort_type != "default":
        sorted_bills = sorted(filter_bills, key=lambda k: k[sort_type])
    else:
        sorted_bills = filter_bills

    url = view_bill_pie(employee['_id'])
    return render_template('employees/view_bills.html', bills=sorted_bills, sort_type=sort_type, filter_type=filter_type, url=url)


def view_bill_pie(_id):
    bills = Bill.all_bills_for_manager(_id)
    # print(bills.count()) - to check if the pymongo cursor returned does not countain any value
    if bills.count() == 0:
        bills = Bill.all_bills_for_employee(_id)

    accept = reject = pending = 0
    for bill in bills:
        print(bill)
        if bill['status'] == 'accept':
            accept = accept + 1
        elif bill['status'] == 'reject':
            reject = reject + 1
        else:
            pending = pending + 1

    sum = accept + pending + reject
    print(sum, accept, reject, pending)
    if sum is not 0:

        labels = "Pending", "Accept", "Reject"
        sizes = [pending / sum, accept / sum, reject / sum]
        # pd.DataFrame(sizes, columns=labels)
        colors = ['gold', 'yellowgreen', 'lightskyblue']
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%.0f%%',
                shadow=True, startangle=90, radius=0.5)
        ax1.axis('equal')
        plt.savefig('plot.png')

        upload_result = upload('plot.png')
        url = upload_result['url']
        thumbnail_url1, options = cloudinary_url(upload_result['public_id'], format="png", crop="fill", width=100,
                                                         height=100)
        # plt.show()
        return url

@bill_blueprint.route('/add', methods=['GET', 'POST'])
@bills_decorators.requires_login
def add_bill():
    # print(session.keys())
    email = session['email']
    employee = Employee.get_by_employee_email(email)
    employee_id = None
    manager_id = None
    if employee is not None:
        employee_id = employee['_id']
        name = employee['name']
        department_id = employee['department_id']
    else:
        manager = Manager.get_by_manager_email(email)
        manager_id = manager['_id']
        name = manager['name']
        department_id = manager['department_id']
    #    print(manager)
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

        if employee is not None:
            Bill.add_bill(bill_type, employee_id, manager_id, department_id, date_of_submission, bill_image_url)
        else:
            Bill.add_bill(bill_type, employee_id, manager_id, department_id, date_of_submission, bill_image_url)

    if employee is not None:
        return render_template('employees/add_bill.html', upload_result=upload_result, url=url,
                               thumbnail_url1=thumbnail_url1, bill_types=bill_types,
                               employee_name=name, department_id=department_id)
    else:
        return render_template('managers/add_bill.html', upload_result=upload_result, url=url,
                               thumbnail_url1=thumbnail_url1, bill_types=bill_types,
                               manager_name=name, department_id=department_id)


@bill_blueprint.route('/delete/<string:bill_id>', methods=['GET'])
@bills_decorators.requires_login
def delete_bill(bill_id):
    Bill.delete(bill_id)
    return redirect(url_for('.view_bills', sort_type="default", filter_type="all"))


@bill_blueprint.route('/editBill/<string:bill_id>', methods=['GET', 'POST'])
@bills_decorators.requires_login
def edit_bill(bill_id):
    bill = Bill.get_by_id(bill_id)
    email = session['email']
    employee = Employee.get_by_employee_email(email)
    manager = None
    if employee is None:
        manager = Manager.get_by_manager_email(email)
        department_id = manager['department_id']
    else:
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

    if employee is not None:
        bill.employee_update_to_db()
        return render_template('employees/edit_bill.html', bill_types=bill_types)
    else:
        bill.manager_update_to_db()
        return render_template('managers/edit_bill.html', bill_types=bill_types)


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
        if 'employee_id' in bill.keys():
            res={}
            res['_id'] = bill['_id']
            res['bill_type'] = bill['bill_type']
            res['max_reimbursement_amount'] = get_bill_amount_by_department_and_type(manager['department_id'], bill['bill_type'])
            res['bill_image_url'] = bill['bill_image_url']
            res['date_of_submission'] = bill['date_of_submission']
            res['status'] = bill['status']
            employee_id = bill['employee_id']
            try:
                employee = Employee.get_by_employee_id(employee_id)
            except BillErrors.NoBills as a:
                raise a.message
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


@bill_blueprint.route('/director/viewBills/<string:sort_type>/<string:filter_type>', methods=['GET'])
@bills_decorators.requires_login
def view_bills_to_director(sort_type, filter_type):
    email = session['email']
    director = Director.get_by_director_email(email)
    filter_bills = None
    if filter_type == "pending" and filter_type is None:
        filter_bills = Bill.all_bills(director['department_id'], "pending")
    else:
        filter_bills = Bill.all_bills(director['department_id'], filter_type)
    response = []
    for bill in filter_bills:
        if 'manager_id' in bill.keys():
            res={}
            res['_id'] = bill['_id']
            res['bill_type'] = bill['bill_type']
            res['max_reimbursement_amount'] = get_bill_amount_by_department_and_type(director['department_id'], bill['bill_type'])
            res['bill_image_url'] = bill['bill_image_url']
            res['date_of_submission'] = bill['date_of_submission']
            res['status'] = bill['status']
            manager_id = bill['manager_id']
            manager = Manager.get_by_manager_id(manager_id)
            res['manager_name'] = manager.name
            res['manager_designation'] = manager.designation
            department = Department.get_by_id(bill['department_id'])
            res['department_name'] = department['name']
            response.append(res)

    sorted_bills = None
    if sort_type == "default":
        sorted_bills = response
    else:
        sorted_bills = sorted(response, key=lambda k: k[sort_type])

    return render_template('directors/view_bills.html', response=sorted_bills, sort_type=sort_type, filter_type=filter_type)


@bill_blueprint.route('/manager/viewMyBills/<string:sort_type>/<string:filter_type>', methods=['GET'])
@bills_decorators.requires_login
def view_manager_bills(sort_type, filter_type):
    email = session['email']
    manager = Manager.get_by_manager_email(email)
    filter_bills = None
    if filter_type == "all":
        filter_bills = Bill.all_bills_for_manager(manager['_id'])
    else:
        filter_bills = Bill.all_bills_for_manager_filter(manager['_id'], filter_type)
    sorted_bills = None
    if sort_type != "default":
        sorted_bills = sorted(filter_bills, key=lambda k: k[sort_type])
    else:
        sorted_bills = filter_bills

    url = view_bill_pie(manager['_id'])
    if url is None:
        url = '#'
    return render_template('managers/view_manager_bills.html', bills=sorted_bills, sort_type=sort_type,
                           filter_type=filter_type, url=url)


@bill_blueprint.route('/manager/accept/<string:bill_id>/<string:type>', methods=['GET', 'POST'])
@bills_decorators.requires_login
def accept_bill(bill_id, type):
    print(type)
    bill = Bill.get_by_id_for_manager(bill_id)
    employee_id = None
    manager_id = None
    if type == "employee":
        employee_id = bill['employee_id']
        email = Employee.get_by_employee_id(employee_id)
    else:
        manager_id = bill['manager_id']
        email = Manager.get_by_manager_id(manager_id)

    reimburse_amount = request.form['reimburse']

    try:
        Bill.isReimbursementAdded(reimburse_amount)
        send_email(email.email, reimburse_amount, "accept")
        Bill.update(bill_id, bill['bill_type'], employee_id, manager_id, bill['department_id'],
                    bill['date_of_submission'], bill['bill_image_url'], "accept")
    except BillErrors.ReimbursementAmountNotAdded as error:
        return error.message

    if type == "employee":
        return redirect(url_for('.view_bills_to_manager', sort_type="default", filter_type="pending"))
    else:
        return redirect(url_for('.view_bills_to_director', sort_type="default", filter_type="pending"))


@bill_blueprint.route('/manager/reject/<string:bill_id>/<string:type>', methods=['GET'])
@bills_decorators.requires_login
def reject_bill(bill_id, type):
    bill = Bill.get_by_id_for_manager(bill_id)
    employee_id = None
    manager_id = None
    if type == "employee":
        employee_id = bill['employee_id']
        email = Employee.get_by_employee_id(employee_id)
    else:
        manager_id = bill['manager_id']
        email = Manager.get_by_manager_id(manager_id)
    send_email(email.email, 0, "reject")

    Bill.update(bill_id, bill['bill_type'], employee_id, manager_id, bill['department_id'],
                bill['date_of_submission'], bill['bill_image_url'], "reject")

    if type == "employee":
        return redirect(url_for('.view_bills_to_manager', sort_type="default", filter_type="pending"))
    else:
        return redirect(url_for('.view_bills_to_director', sort_type="default", filter_type="pending"))