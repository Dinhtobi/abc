from flask import Flask
from flask import request
from flask_cors import CORS , cross_origin 
import os
import subprocess
from subprocess import Popen
import glob

import base64
from io import BytesIO
from PIL import Image
#Khởi tạo Flask Server Backend
app = Flask(__name__)

#Apply Flask CORS
CORS(app)
app.config['CORS_HEADERS']  ='Content-Type'
app.config['UPLOAD_FOLDER'] = "static"

def save_image(face_base64):
    img_data = base64.b64decode(face_base64)
    image = Image.open(BytesIO(img_data))
    folder_path = "test_image"
    jpg_count = len(glob.glob(folder_path + "/*.jpg"))
    path_image = folder_path + "/anh{}".format(jpg_count+1)+".jpg"
    image.save(path_image)
    return path_image

@app.route('/predict' , methods= ['POST'])
@cross_origin(origins='*')

def predict_YOLOv7_proces():

    face_base64 = request.values.get('facebase64')
    path_image = save_image(face_base64)
    subprocess.Popen(["F:\PBL5\YOLOv7_train\yolov7\.venv\Scripts\python", 'detect.py','--weights','runs/train/exp4/weights/last.pt', '--source',path_image ])
     
    return "test"
   


#Start Backend
if __name__ == '__main__':
    app.run(host='0.0.0.0' , port = '6868',use_reloader=True)
    
