import myYolov7
import os
import cv2
import matplotlib.pyplot as plt
model = myYolov7.my_yolov7('last.pt','cpu',0.6)

def predict_YOLOv7_proces(folderTrain='train_img' , folderOutput='output_img'):
    
    for pathfolder in os.listdir(folderTrain):
        try:
            count = 0
            if os.path.exists( folderOutput + '/' + pathfolder):
                os.rmdir( folderOutput + '/' + pathfolder)
            os.mkdir( folderOutput + '/' + pathfolder)
            savepath = folderOutput + '/' + pathfolder +'/image.jpg'
            for pathfile in os.listdir(folderTrain+ '/' + pathfolder):
                count +=1
                imgs =  folderTrain+'/' + pathfolder +'/' + pathfile  
                print(imgs, savepath , count)
                model.detect(imgs,savepath,count)
        except:
            print("Thư mục bạn dùng để cắt ảnh đã tồn tại và còn ảnh bên trong!")        

predict_YOLOv7_proces()