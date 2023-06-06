from flask import Blueprint, render_template, request, redirect, url_for, jsonify,json,Response,abort
from webmodel.models import *
import myYolov7
import os
import test
import glob
from datetime import datetime
from webcontroller.user_controller import get_users
models = test.face_regconie()
model = myYolov7.my_yolov7('last.pt','cpu',0.6)
session_controller = Blueprint('session_controller', __name__, url_prefix='/api/session')


def save_image(image):
    folder_path = "test_image"
    image_count = len(glob.glob(folder_path + "/*.jpg"))
    path_video = folder_path + "/anh{}".format(image_count+1)+".jpg"
    image.save(path_video)
    return path_video
@session_controller.route('/predict' , methods= ['POST'])
#@cross_origin(origins='*')

def predict_image():
    try:
        file = request.files['file']
        if file :
            path_file =  save_image(file)
            imgs = path_file 
            listfile = os.listdir('test_image')
            count = len(listfile)
            folderpath = 'output_img'
            savepath =  folderpath +'/image.jpg'

            users = Users.query.all()
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            current_date = date.today()
            users_recognition = []
            user_session = Sessions.query.all()
            getwork_schedule = Work_schedule.query.filter(Work_schedule.start_time <= current_time, Work_schedule.end_time >= current_time).filter(Work_schedule.work_date == current_date).all()
            for i in users:
                for k in getwork_schedule:
                    if i.id_department == k.id_department:
                        users_recognition.append(i)
            for i in getwork_schedule:
                for j in user_session:
                    for k in users_recognition:
                        if k.id_user == j.id_user and i.id_work_schedule == j.id_work_schedule:
                            users_recognition.remove(k)
            result,img1,bounding_box =  model.detect(imgs,savepath,count)
            idpeople ,path = models.regconie(path_file,bounding_box, img1,users_recognition)
            os.remove(path_file)
            print(idpeople)
            if idpeople :
                saveSession(idpeople,getwork_schedule,path)
                return path
                           
            else :
                return "False"

    except Exception as e:
        print(e)
        return e 
    
def saveSession(idpeople,getwork_schedule,savepath):
    try:
        users = Users.query.all()
        for i in users:
            for j in idpeople:
                for k in getwork_schedule:
                    if str(i.id_user) == j and i.id_department == k.id_department:
                        path = "http://0.0.0.0:6868/" + savepath
                        newsesstion = Sessions( id_user = i.id_user ,id_work_schedule = k.id_work_schedule,image_url = path , token ="Add")
                        db.session.add(newsesstion)
                        db.session.commit()
        return "Thành công"
    except Exception as e:
        print(e)
@session_controller.route('/' , methods= ['POST'])
def getEmployee():
    try:
        id_employee = request.json['id_employee']
        start_day = request.json['start_day'].encode('utf8')
        end_day = request.json['end_day'].encode('utf8')
        user = Users.query.filter_by(id_user = id_employee).first()
        work_schedules = Work_schedule.query.filter(Work_schedule.work_date <= end_day, Work_schedule.work_date  >= start_day).filter_by(id_department = user.id_department).order_by(Work_schedule.work_date.desc()).all()
        listsessionemployee =[]
        for i in work_schedules:
            session = Sessions.query.filter_by(id_work_schedule = i.id_work_schedule).filter_by(id_user = user.id_user).first()
            if session:
                listsessionemployee.append(serialize_employstatus(session,user , i))
            else :
                listsessionemployee.append(serialize_employstatus(None,user , i))
        return jsonify(listsessionemployee)
        
    except Exception as e:
        print(e)
def serialize_employstatus( session ,user , work_schedule):
    if session != None:
        if session.session_id :
            status = 1
            time = session.created_at
    else :
        status = 0 
        time = ''
    return{
        'date': work_schedule.work_date,
        'id' : user.id_user,
        'img_avatar' : user.img_avatar,
        'roll_name' : user.rolename,
        'name' : user.name,
        'status' : status,
        'time': time,
    }  