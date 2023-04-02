from flask import Flask ,render_template
from flask import request
from flask_cors import CORS , cross_origin 
import os
import glob
import myYolov7
import train_main
import test
from webmodel.models import db
from webroute.route import route_bp
from flask_migrate import Migrate
from flask import Blueprint

#Khởi tạo Flask Server Backend
app = Flask(__name__)
app.config.from_object('config')
#Apply Flask CORS
CORS(app)
app.config['CORS_HEADERS']  ='Content-Type'
app.config['UPLOAD_FOLDER'] = "static"
db.init_app(app)

migrate = Migrate(app, db)
#model = myYolov7.my_yolov7('last.pt','cpu',0.6)
#route_bp = Blueprint('route_bp', __name__)
app.register_blueprint(route_bp, url_prefix='/')



@app.route('/' , methods= ['POST' , 'GET'])
@cross_origin(origins='*')

def trangchu():
    return render_template('index.html')


@app.route('/train' , methods= ['POST'])
@cross_origin(origins='*')

def TrainImage():
    folderTrain = 'test_image/'
    file = request.files['file']
    pathfolder = file.filename.split('/')[0]
    if os.path.exists( folderTrain + '/' + pathfolder):
        os.rmdir( folderTrain + '/' + pathfolder)
    os.mkdir( folderTrain + '/' + pathfolder)
    count =0 
    for file in request.files.getlist('file'):
        savepath = folderTrain+ file.filename
        count +=1
        #imgs =  folderTrain+'/' + pathfolder +'/' + pathfile  
        print(savepath, savepath , count)
        #model.detect(savepath,savepath,count)
    train_main.Train()
    return 'Upload completed'
#Start Backend
if __name__ == '__main__':
    app.run(host='0.0.0.0' , port = '6868'#,use_reloader=True
            )
    
