import torch
import numpy as np
import math
import cv2
from models.experimental import attempt_load
from utils.general import check_img_size,set_logging ,non_max_suppression, scale_coords, xyxy2xywh
from utils.plots import plot_one_box   
from utils.datasets import  LoadImages
from numpy import random
import time
from utils.torch_utils import select_device ,time_synchronized
class my_yolov7():
    def __init__(self, weights,device,conf_thres,img_size=640):
        set_logging()
        self.device = select_device(device)
        self.half = self.device.type != 'cpu'  # half precision only supported on CUDA
        self.conf_thres = conf_thres
        self.model = attempt_load(weights, map_location=self.device)  # load FP32 model
        self.stride = int(self.model.stride.max())  # model stride
        self.imgsz = check_img_size(img_size, s=self.stride)  # check img_size # check image size
        
    def detect(self, source,savepath,count):
        self.source = source
        dataset = LoadImages(source, img_size=self.imgsz, stride=self.stride)
        names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

        for path, img, im0s, vid_cap in dataset:
            img = torch.from_numpy(img).to(self.device)
            img = img.half() if self.half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # # Warmup
            # if self.device.type != 'cpu' and (old_img_b != img.shape[0] or old_img_h != img.shape[2] or old_img_w != img.shape[3]):
            #     old_img_b = img.shape[0]
            #     old_img_h = img.shape[2]
            #     old_img_w = img.shape[3]
            #     for i in range(3):
            #         self.model(img, augment=opt.augment)[0]

            # Inference
            pred = self.model(img, augment=False)[0]


            # Apply NMS
            pred = non_max_suppression(pred,self.conf_thres, 0.45, classes=None, agnostic=False)
 
            # Process detections
            for i, det in enumerate(pred):  # detections per image
                
                p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

                # p = Path(p)  # to Path
                # save_path = str(save_dir / p.name)  # img.jpg
                # txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # img.txt
             
                #gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                    # Print results
                    # for c in det[:, -1].unique():
                    #     n = (det[:, -1] == c).sum()  # detections per class
                    #     s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string
                    index = 0
                    # Write results
                    for *xyxy, conf, cls in reversed(det):
                        
                        #xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        #line = (cls, *xywh, conf) if False else (cls, *xywh)  # label format
                        # with open(txt_path + '.txt', 'a') as f:
                        #     f.write(('%g ' * len(line)).rstrip() % line + '\n')
                        index+=1
                        label = f'{names[int(cls)]} {conf:.2f}'
                        crop_img = im0[int(xyxy[1]):int(xyxy[3]), int(xyxy[0]):int(xyxy[2])]
                        #print(int(xyxy[1]),int(xyxy[3]),int( xyxy[0]),int(xyxy[2]))
                        cv2.imwrite(savepath.split('.jpg')[0]+'_{}_{}.jpg'.format(count,index), crop_img)
            
                        plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=1)
                    im0 = np.asarray(im0)
                return im0 ,det