from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
from src.models.billTypes.billType import BillType

__author__ = 'ishween'

billType_blueprint = Blueprint('billType', __name__)


# @billType_blueprint.route('/')
# def index():
#     BillType.all()


#@billType_blueprint.route('/add', methods = ['GET', 'POST'])
#def addBill():
#    if request.method == 'POST':
#        department_id = request.form['department_id']
#        type = request.form['type']
#        reimbursement = request.form['reimbursement']
#
#         BillType.add_bill_type(department_id, type, reimbursement)


def add_bill_type(department_id, type, reimbursement):
    BillType.add_bill_type(department_id, type, reimbursement)


def show_all_bill_type(department_id):
    BillType.all(department_id)


def delete_bill_type(bill_type_id):
    BillType.get_by_id(bill_type_id).delete()


@billType_blueprint.route('/edit/<string:billType_id>', methods=['GET', 'POST'])
def edit_bill_type(billType_id):
    billType = BillType.get_by_id(billType_id)
    if request.method == 'POST':
        reimbursement = request.form['reimbursement']

        billType.reimbursement = reimbursement

        billType.update_to_db()
        return redirect(url_for('admin.view_bill_types_admin'))
    return render_template('bill_types/edit_bill.html')


@billType_blueprint.route('/deleteBillType/<string:billType_id>', methods=['GET'])
def delete_bill_type(billType_id):
    BillType.get_by_id(billType_id).delete()
    return redirect(url_for('admin.view_bill_types_admin'))


def get_bills_type_by_department(department_id):
    billTypes = BillType.all(department_id)
    response = []
    for b in billTypes:
        res = {}
        res['_id'] = b._id
        res['type'] = b.type
        res['reimbursement'] = b.reimbursement
        response.append(res)
    return response