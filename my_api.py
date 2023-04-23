from flask import Flask ,render_template
from flask import request
from flask_cors import CORS , cross_origin 
import os
import train_main
# from webroute.route import route_bp
from flask_migrate import Migrate
from flask import Blueprint
from webmodel.models import db
from webcontroller.user_controller import user_controller ,mail
from webcontroller.department_controller import department_controller
from webcontroller.session_controller import session_controller
from webcontroller.work_schedule_controller import work_schedule_controller

#Khởi tạo Flask Server Backend
app = Flask(__name__)
app.config.from_object('config')
#Apply Flask CORS
CORS(app)
app.config['CORS_HEADERS']  ='Content-Type'
app.config['UPLOAD_FOLDER'] = "static"
mail.init_app(app)
db.init_app(app)

migrate = Migrate(app, db)
app.register_blueprint(user_controller)
app.register_blueprint(department_controller)
app.register_blueprint(session_controller)
app.register_blueprint(work_schedule_controller)



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
    app.run(host='0.0.0.0' , port = '6868',#use_reloader=True
            )
    
