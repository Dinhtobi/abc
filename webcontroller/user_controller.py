# controllers.py

from flask import Blueprint, render_template, request, redirect, url_for, jsonify,json,Response,abort
from webmodel.models import Users,db
import datetime
import random
import string
from flask_mail import Mail, Message
import bcrypt
mail = Mail()
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
    if not request.json or not 'name' in request.json or not 'email' in request.json or not 'password' in request.json or not 'rolename' in request.json:
        abort(400)
    salt = bcrypt.gensalt()
    bytes = request.json['password'].encode('utf-8')
    hashed_password = bcrypt.hashpw(bytes, salt)
    user = Users(name=request.json['name'], email=request.json['email'], password=hashed_password, rolename=request.json['rolename'])
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
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(request.json['password'], salt)
        user.password = hashed_password
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
        user = Users.query.filter_by(email = email).first()
        if bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8')):

            if user:
                return jsonify(user.serialize())
            else: return  "null"
        else: 
            return jsonify({'message': 'Wrong password'}), 400
    except Exception as e:
        print(str(e))
        return "Error"

@user_controller.route('/changepassword', methods = ['POST'])
def user_rspassword():
    
    try:
        email = request.json['email']
        newpassword = request.json['newpassword']
        oldpassword = request.json['oldpassword']
        token = request.json['token']
        if token != 'null' and oldpassword == 'null':
            user = Users.query.filter_by(email = email).first()
            if email != user.email:
                return jsonify({'message': 'User not found'}), 404
        
            if token != user.token:
                return jsonify({'message': 'Invalid token'}), 400
            if user:
                token = generate_token(16)
                user.email = email 
                user.password = newpassword
                user.token = token
                db.session.commit()
                return "True"
            else: return "False"
        else :
            user = Users.query.filter_by(email = email).filter_by(password = oldpassword).first()
            if email != user.email:
                return jsonify({'message': 'User not found'}), 404
            if user:
                token = generate_token(16)
                user.email = email 
                user.password = newpassword
                user.token = token
                db.session.commit()
                return "True"
            else: return "False"
    except Exception as e:
        print(str(e))
        return "False" 

# Generate a random string of letters and digits
def generate_token(length):
    letters_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_digits) for i in range(length))


def send_reset_email(email, token):
    msg = Message('password Reset', sender = 'dinhnguyen2002asd@gmail.com', recipients = [email])
    msg.body = f'Please click on this link to reset your password: token={token}'
    mail.send(msg)

# Reset password API
@user_controller.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.json['email']
    user = Users.query.filter_by(email = email).first()
    if email != user.email:
        return jsonify({'message': 'User not found'}), 404
    
    # Generate a unique token
    token = generate_token(6)
    if user:
        user.token = token
        db.session.commit()
    # Send a password reset email
    send_reset_email(email, token)
    
    return jsonify({'message': 'password reset email sent'}), 200
