import json

from src.models.department.department import Department
from flask import Flask, render_template, request, Blueprint

department_blueprint = Blueprint('department', __name__)


def add_department(company_id, name):
    Department.add_department(company_id, name)


#@department_blueprint.route('/viewDepartments', methods = ['GET'])
def view_departments(company_id):
    print(company_id)
    departments = Department.get_all(company_id)
    return departments

def get_department(department_id):
    department = Department.get_by_id(department_id)
    return department
