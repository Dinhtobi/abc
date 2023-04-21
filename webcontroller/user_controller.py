# controllers.py

from flask import Blueprint, render_template, request, redirect, url_for, jsonify,json,Response,abort
from webmodel.models import Users,db
import datetime

user_controller = Blueprint('user_controller', __name__, url_prefix='/api/users')

@user_controller.route('/', methods=['GET'])
def get_users():
    users = Users.query.all()
    user_list = [user.serialize() for user in users]
    return jsonify(users=user_list)

@user_controller.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = Users.query.get_or_404(user_id)
    return jsonify(user=user.serialize())


@user_controller.route('/create', methods=['POST'])
def create_user():
    if not request.json or not 'name' in request.json or not 'email' in request.json or not 'password' in request.json or not 'role' in request.json:
        abort(400)
    user = Users(name=request.json['name'], email=request.json['email'], password=request.json['password'], role=request.json['role'])
    if 'address' in request.json:
        user.address = request.json['address']
    if 'date_of_birth' in request.json:
        user.date_of_birth = datetime.strptime(request.json['date_of_birth'], '%Y-%m-%d').date()
    if 'img_avatar' in request.json:
        user.img_avatar = request.json['img_avatar']
    if 'id_department' in request.json:
        user.id_department = request.json['id_department']
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 201

@user_controller.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = Users.query.get_or_404(user_id)
    if not request.json:
        abort(400)
    if 'name' in request.json:
        user.name = request.json['name']
    if 'email' in request.json:
        user.email = request.json['email']
    if 'password' in request.json:
        user.password = request.json['password']
    if 'role' in request.json:
        user.role = request.json['role']
    if 'address' in request.json:
        user.address = request.json['address']
    if 'date_of_birth' in request.json:
        user.date_of_birth = datetime.strptime(request.json['date_of_birth'], '%Y-%m-%d').date()
    if 'img_avatar' in request.json:
        user.img_avatar = request.json['img_avatar']
    if 'id_department' in request.json:
        user.id_department = request.json['id_department']
    db.session.commit()
    return jsonify(user.serialize())

@user_controller.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'result': True})

@user_controller.route('/login', methods = ['POST'])
def user_login():
    email = request.form['email']
    password = request.form['password']
    try:
        user = Users.query.filter_by(Email = email).filter_by(Password = password).first()
        if user:
            return jsonify(user.serialize())
        else: return  "null"
    except Exception as e:
        print(str(e))
        return "Error"

@user_controller.route('/resetpass', methods = ['POST'])
def user_rspassword():
    email = request.form['email']
    newpassword = request.form['newpassword']
    oldpassword = request.form['oldpassword']
    try:
        user = Users.query.filter_by(Email = email).filter_by(Password = oldpassword).first()
        if user:
            user.Email = email 
            user.Password = newpassword
            db.session.commit()
            return "True"
        else: return "False"
    except Exception as e:
        print(str(e))
        return "False"

