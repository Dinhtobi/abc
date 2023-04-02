from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import cv2
import numpy as np
import facenet
import myYolov7
import os
import time
import pickle
import imageio.v2 as imageio
from PIL import Image
import tensorflow.compat.v1 as tf
class face_regconie():
    def __init__(self):
        self.video= 0
        self.modeldir = './model/20180402-114759.pb'
        self.classifier_filename = './class/classifier.pkl'
        self.npy='./npy'
        self.train_img="./train_img"
        with tf.Graph().as_default():
            self.gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.6)
            self.sess = tf.Session(config=tf.ConfigProto(gpu_options=self.gpu_options, log_device_placement=False))
            with self.sess.as_default():
                self.margin = 44
                self.batch_size =100 #1000
                self.image_size = 182
                self.input_image_size = 160
                self.HumanNames = os.listdir(self.train_img)
                self.HumanNames.sort()
                print('Loading Model')
                facenet.load_model(self.modeldir)
                self.images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
                self.embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
                self.phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
                self.embedding_size = self.embeddings.get_shape()[1]
                classifier_filename_exp = os.path.expanduser(self.classifier_filename)
                with open(classifier_filename_exp, 'rb') as infile:
                    (self.model, self.class_names) = pickle.load(infile,encoding='latin1')
                
                video_capture = cv2.VideoCapture(self.video)
    def regconie(self,path_img , boundingbox):
            
        
                print('Start Recognition')
                # while True:
                # ret, frame = video_capture.read()
                frame=imageio.imread(path_img)
                
                #frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)    #resize frame (optional)
                timer =time.time()
                if frame.ndim == 2:
                    frame = facenet.to_rgb(frame)
                    
                savepath = 'output_img/image.jpg'
                imgsource = path_img
                bounding_boxes = boundingbox
                faceNum = bounding_boxes.shape[0]
                if faceNum > 0:
                    det = bounding_boxes[:, 0:4]
                    img_size = np.asarray(frame.shape)[0:2]
                    cropped = []
                    scaled = []
                    scaled_reshape = []
                    for i in range(faceNum):
                        emb_array = np.zeros((1, self.embedding_size))
                        xmin = int(det[i][0])
                        ymin = int(det[i][1])
                        xmax = int(det[i][2])
                        ymax = int(det[i][3])
                        try:
                            # inner exception
                            if xmin <= 0 or ymin <= 0 or xmax >= len(frame[0]) or ymax >= len(frame):
                                print('Face is very close!')
                                continue
                            cropped.append(frame[ymin:ymax, xmin:xmax,:])
                            cropped[i] = facenet.flip(cropped[i], False)
                            scaled.append(np.array(Image.fromarray(cropped[i]).resize((self.image_size, self.image_size))))
                            scaled[i] = cv2.resize(scaled[i], (self.input_image_size,self.input_image_size),
                                                    interpolation=cv2.INTER_CUBIC)
                            scaled[i] = facenet.prewhiten(scaled[i])
                            scaled_reshape.append(scaled[i].reshape(-1,self.input_image_size,self.input_image_size,3))
                            feed_dict = {self.images_placeholder: scaled_reshape[i], self.phase_train_placeholder: False}
                            
                            emb_array[0, :] = self.sess.run(self.embeddings, feed_dict=feed_dict)
                            predictions = self.model.predict_proba(emb_array)
                            best_class_indices = np.argmax(predictions, axis=1)
                            best_class_probabilities = predictions[np.arange(len(best_class_indices)), best_class_indices]
                            if best_class_probabilities>0.7:
                                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)    #boxing face
                                for H_i in self.HumanNames:
                                    if self.HumanNames[best_class_indices[0]] == H_i:
                                        result_names = self.HumanNames[best_class_indices[0]]
                                        print("Predictions : [ name: {} , accuracy: {:.3f} ]".format(self.HumanNames[best_class_indices[0]],best_class_probabilities[0]))
                                        cv2.rectangle(frame, (xmin, ymin-20), (xmax, ymin-2), (0, 255,255), -1)
                                        cv2.putText(frame, result_names, (xmin,ymin-5), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                                    1, (0, 0, 0), thickness=1, lineType=1)
                                
                                        
                            else :
                                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                                cv2.rectangle(frame, (xmin, ymin-20), (xmax, ymin-2), (0, 255,255), -1)
                                cv2.putText(frame, "?", (xmin,ymin-5), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                                    1, (0, 0, 0), thickness=1, lineType=1)
                        except:   
                            
                            print("error")
                            
            
