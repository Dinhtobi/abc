from flask import render_template , redirect , url_for , request , abort, jsonify
from webmodel.models import *

def User_Login(email , password):
    try:
        user = Users.query.filter_by(Email = email).filter_by(Password = password).first()
        if user:
            check = "TRUE"
        else: check = "False"
        return check
    except Exception as e:
        print(str(e))
        return "Error"


def User_ResetPass(id,email , password):
    try:
        user = db.session.query(Users).filter_by(id_user = id).first() 
        if user:
            user.Email = email 
            user.Password = password
            db.session.commit()
            return "True"
        else: return "False"
        

    except Exception as e:
        print(str(e))
        return "False"
    
def department_getall():
    try:
        department = Department.query.all()
        
        return jsonify(json_list =[i.serialize() for i in department])
    except Exception as e:
            print(str(e))
            return "Error Controller Department"
    
def detaildepartment_getbyid_department(id_department):
    try:
        detaildepartment = DetailDepartment.query.filter_by(id_department = id_department).all()
        users = Users.query.all()
        listuser = []
        for i in detaildepartment:
            for j in users :
                if i.id_user == j.id_user:
                    listuser.append(j.serialize())
        return jsonify(listuser)
    except Exception as e:
            print(str(e))
            return "Error controller detaildepartment"