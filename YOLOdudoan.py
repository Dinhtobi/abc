import cv2

# Đường dẫn tới hình ảnh
image_path = "anh1.jpg"

# Đọc hình ảnh
image = cv2.imread(image_path)

# Tọa độ của bounding box (x, y, width, height)
bounding_box1 = (235, 225, 347, 494)
bounding_box2 = (239,236 , 347, 494)
# Tạo một hình chữ nhật để vẽ bounding box
# x, y, width, height = bounding_box
# cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)

# Hiển thị hình ảnh với bounding box
# cv2.imshow("Image with Bounding Box", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

def intersection_area(box1, box2):
    # Tính toán tọa độ của bounding box giao nhau
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[0] + box1[2], box2[0] + box2[2])
    y2 = min(box1[1] + box1[3], box2[1] + box2[3])

    # Kiểm tra nếu không có phần giao nhau
    if x2 < x1 or y2 < y1:
        return 0

    # Tính toán diện tích giao nhau
    intersection_width = x2 - x1
    intersection_height = y2 - y1
    intersection_area = intersection_width * intersection_height

    return intersection_area

def total_area(box1, box2):
    area1 = box1[2] * box1[3]  # Diện tích của bounding box thứ nhất
    area2 = box2[2] * box2[3]  # Diện tích của bounding box thứ hai
    total_area = area1 + area2  # Tổng diện tích của cả hai bounding box
    return total_area
area = intersection_area(bounding_box1, bounding_box2)
total_area = total_area(bounding_box1, bounding_box2)
total_area -=area
print("Diện tích giao nhau:", area)
print("Tổng diện tích:", total_area)
print("IoU:", area/total_area)
