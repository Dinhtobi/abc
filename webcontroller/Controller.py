from flask import render_template , redirect , url_for , request , abort, jsonify
from webmodel.models import *
from datetime import datetime
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
    

def saveFace(savepath, id_se , id_myuser):
    try:
        path = "http://0.0.0.0:6868/" + savepath
        face = faces(id_user = id_myuser , image_url = path , id_session = id_se)
        db.session.add(face)
        db.session.commit()
    except Exception as e:
        print(e)

def saveSession(Namepeople,savepath):
    try:
        users = Users.query.all()
        
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = date.today()
        getwork_schedule = work_schedule.query.filter(work_schedule.start_time <= current_time, work_schedule.end_time >= current_time).filter(work_schedule.work_date == current_date).first()
        for i in users:
            for j in Namepeople:
                if i.Name == j:
                    newsesstion = sessions( id_user = i.id_user ,id_work_schedule = getwork_schedule.id_work_schedule , token ="Add")
                    db.session.add(newsesstion)
                    db.session.commit()
                    saveFace(savepath, newsesstion.session_id, i.id_user)
        return "Thành công"
    except Exception as e:
        print(e)

def getimagebyface(id_face):
    try:
        face = faces.query.filter_by(id_face = id_face).first()
        if face :
            return face.image_url 
        else:
            return "null"

    except Exception as e:
        print(e)