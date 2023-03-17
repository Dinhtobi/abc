from models.yolo import Model
import cv2
import torch
import detect
model = Model(cfg='models/face-yolov7.yaml', ch=3, nc=1 ,anchors=None).to(torch.device('cpu'))
model.load_state_dict(torch.load('last.pt', map_location=torch.device('cpu')))
model.eval()
img = cv2.imread('test_image/anh1.jpg') # đọc ảnh đầu vào

def detect_batch(img):
    detections = []
    for img in images:
        # Chuyển đổi hình ảnh thành định dạng PIL
        img_pil = Image.fromarray(img)
        # Thực hiện phát hiện đối tượng trên hình ảnh
        results = detect.detect(model, img_pil, device='cpu')
        detections.append(results.xyxy[0].cpu().numpy())
    return detections

# Tải một lô (batch) các hình ảnh
images = load_images_from_folder("path/to/images")

# Thực hiện phát hiện đối tượng trên lô (batch) các hình ảnh
detections = detect_batch(images)