from flask import Blueprint
from flask import render_template , redirect , url_for , request , abort, jsonify ,send_from_directory
import myYolov7
import os
from webcontroller.Controller import *
import test
import glob
models = test.face_regconie()
model = myYolov7.my_yolov7('last.pt','cpu',0.6)
route_bp = Blueprint('route_bp', __name__)


def save_image(image):
    folder_path = "test_image"
    image_count = len(glob.glob(folder_path + "/*.jpg"))
    path_video = folder_path + "/anh{}".format(image_count+1)+".jpg"
    image.save(path_video)
    return path_video
@route_bp.route('/predict' , methods= ['POST'])
#@cross_origin(origins='*')

def predict_image_YOLOv7_proces():
    try:
        file = request.files['file']
        if file :
            path_file =  save_image(file)
            imgs = path_file 
            listfile = os.listdir('test_image')
            count = len(listfile)
            savepath = 'output_img/image.jpg'
            result,img1,bounding_box =  model.detect(imgs,savepath,count)
            Namepeople ,savepath = models.regconie(path_file,bounding_box, img1)
            if Namepeople :
                os.remove(path_file)
                saveSession(Namepeople,savepath)
                return "True"
            else :
                return "False"

    except Exception as e:
        print(e)
        return e 
        
@route_bp.route('/getimage' , methods= ['GET'])
#@cross_origin(origins='*')

def get_image():
    try:
        id_face = request.form['id_face']
        if id_face :
            face = getimagebyface(id_face)
            if face :
                return face
            else :
                return "False"

    except Exception as e:
        print(e)
        return e 
    
