from flask import render_template , redirect , url_for , request , abort, jsonify
from webmodel.models import *
from datetime import datetime



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


def getallSessionbyPageandiddepartment(id_department , page):
    try:
        users = Users.filter_by(id_department = id_department)
        if users :
            now = datetime.datetime.now()
            five_days_ago = now - datetime.timedelta(days=page*5)
            formatted_timed = five_days_ago.strftime("%Y-%m-%d")
            formatted_time = now.strftime("%Y-%m-%d")
            Sessions = sessions.query.filter(sessions.created_at <= formatted_time, sessions.created_at >= formatted_timed).all()
            
        else :
            return 'null'
    except Exception as e:
        print(e)