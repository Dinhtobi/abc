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
            result,img1,bounding_box =  model.detect(imgs,savepath,count)
            Namepeople ,path = models.regconie(path_file,bounding_box, img1)
            if Namepeople :
                os.remove(path_file)
                
                saveSession(Namepeople,path)
                return "True"
                           
            else :
                return "False"

    except Exception as e:
        print(e)
        return e 
    
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
                    path = "http://0.0.0.0:6868/" + savepath
                    newsesstion = sessions( id_user = i.id_user ,id_work_schedule = getwork_schedule.id_work_schedule,image_url = path , token ="Add")
                    db.session.add(newsesstion)
                    db.session.commit()
        return "Thành công"
    except Exception as e:
        print(e)

