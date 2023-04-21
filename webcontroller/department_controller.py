from flask import Blueprint, render_template, request, redirect, url_for, jsonify,json,Response,abort
from webmodel.models import Department,db,Users


department_controller = Blueprint('department_controller', __name__, url_prefix='/api/departments')

@department_controller.route('/', methods=['GET'])
def get_departments():
    departments = Department.query.all()
    department_list = [department.serialize() for department in departments]
    return jsonify(department=department_list)

@department_controller.route('/<int:id_department>', methods=['GET'])
def get_department(id_department):
    department = Department.query.get_or_404(id_department)
    return jsonify(department=department)

@department_controller.route('/users/<int:id_department>', methods=['GET'])
def get_users_id_departmnet(id_department):
    users = Users.query.filter_by(id_department=id_department).all()
    user_list = [user.serialize() for user in users]
    return jsonify(users=user_list)