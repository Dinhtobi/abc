from flask import Blueprint
from flask import render_template , redirect , url_for , request , abort, jsonify
import myYolov7
import os
from webcontroller.Controller import *
import test
import glob
models = test.face_regconie()
model = myYolov7.my_yolov7('last.pt','cpu',0.6)
route_bp = Blueprint('route_bp', __name__)

@route_bp.route('/login', methods = ['POST'])
def user_login():
    email = request.form['email']
    password = request.form['password']
    return User_Login(email, password)

@route_bp.route('/resetpass', methods = ['POST'])
def user_rspassword():
    email = request.form['email']
    password = request.form['password']
    id_user = request.form['id_user']
    return User_ResetPass(id_user,email, password)

@route_bp.route('/departmentgetall', methods = ['GET'])
def department_getall():
    try:
        department = department_getall()
        return department
    except Exception as e:
            print(str(e))
            return "Error3"
    
@route_bp.route('/getbyid_department', methods = ['POST'])
def detaildepartment_getbyid_department():
    try:
        id_department = request.form['id_department']
        department = detaildepartment_getbyid_department(id_department)
        return department
    except Exception as e:
            print(str(e))
            return "Error3"

def save_image(image):
    folder_path = "test_image"
    image_count = len(glob.glob(folder_path + "/*.jpg"))
    path_video = folder_path + "/anh{}".format(image_count+1)+".jpg"
    image.save(path_video)
    return path_video
@route_bp.route('/predict' , methods= ['POST'])
#@cross_origin(origins='*')

def predict_image_YOLOv7_proces():

    file = request.files['file']
    path_file =  save_image(file)
    imgs = path_file 
    listfile = os.listdir('test_image')
    count = len(listfile)
    savepath = 'output_img/image.jpg'
    result,bounding_box =  model.detect(imgs,savepath,count)
    models.regconie(path_file,bounding_box)
    return "success"
