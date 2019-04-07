from flask import Blueprint, request, url_for, render_template
from werkzeug.utils import redirect
from src.models.billTypes.billType import BillType
import src.decorators as bill_type_decorators
from src.models.admins.views import get_by_email_company_id
from src.models.department.views import view_departments, get_department

__author__ = 'ishween'

billType_blueprint = Blueprint('billType', __name__)


@billType_blueprint.route('/viewBillTypes/<string:sort_type>/<string:filter_type>', methods=['GET'])
@bill_type_decorators.requires_login
def view_bill_types_admin(sort_type, filter_type):
    company_id = get_by_email_company_id()
    departments = view_departments(company_id)
    response = []
    types = []
    department_response = []

    for department in departments:
        department_response.append(department)

    if filter_type.startswith("department"):
        department_id = filter_type[10:]
        bills_type = get_bills_type_by_department(department_id)
        department = get_department(department_id)
        res = {}
        res['department_id'] = department_id
        res['department_name'] = department['name']
        res['bills_type'] = []
        billtypes = []

        for billtype in bills_type:
            billtypes.append(billtype)
            if billtype['type'] not in types:
                types.append(billtype['type'])

        if sort_type != "default":
            res['bills_type'] = sorted(billtypes, key=lambda k: k[sort_type])
        else:
            res['bills_type'] = billtypes
        response.append(res)
    else:
        for department in department_response:
            res={}
            res['department_id'] = department['_id']
            res['department_name'] = department['name']
            res['bills_type'] = []
            billtypes = []

            bills_type = get_bills_type_by_department(department['_id'])

            for billtype in bills_type:
                if filter_type != "default" and filter_type == billtype['type']:
                    billtypes.append(billtype)
                elif filter_type == "default":
                    billtypes.append(billtype)
                if billtype['type'] not in types:
                    types.append(billtype['type'])

            if sort_type != "default":
                res['bills_type'] = sorted(billtypes, key=lambda k: k[sort_type])
            else:
                res['bills_type'] = billtypes
            response.append(res)

    response = sorted(response, key=lambda k: k['department_name']) #alphabetical order

    return render_template('admins/show_bill_types.html', response=response, department_response=department_response, types=types, sort_type=sort_type, filter_type=filter_type)


@billType_blueprint.route('/addBillType', methods=['GET', 'POST'])
@bill_type_decorators.requires_login
def add_a_bill_type():
    company_id = get_by_email_company_id()
    departments = view_departments(company_id)
    if request.method == 'POST':
        department_id = request.form['department_id']
        type = request.form['type']
        reimbursement = request.form['reimbursement']

        # add_bill_type(department_id, type, reimbursement)
        BillType.add_bill_type(department_id, type, reimbursement)

    return render_template('admins/add_bill_type.html', departments=departments)


@billType_blueprint.route('/edit/<string:billType_id>', methods=['GET', 'POST'])
def edit_bill_type(billType_id):
    billType = BillType.get_by_id(billType_id)
    if request.method == 'POST':
        reimbursement = request.form['reimbursement']

        billType.reimbursement = reimbursement

        billType.update_to_db()
        return redirect(url_for('billType.view_bill_types_admin', sort_type="default", filter_type="default"))
    return render_template('admins/edit_bill_type.html')


@billType_blueprint.route('/deleteBillType/<string:billType_id>', methods=['GET'])
def delete_bill_type(billType_id):
    BillType.get_by_id(billType_id).delete()
    return redirect(url_for('billType.view_bill_types_admin', sort_type="default", filter_type="default"))


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


def get_bill_amount_by_department_and_type(department_id, bill_type):
    return BillType.get_amount(department_id, bill_type)['reimbursement']
