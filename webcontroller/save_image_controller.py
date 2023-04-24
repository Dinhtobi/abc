from flask import Blueprint, render_template, request, redirect, url_for, jsonify,json,Response,abort
from webmodel.models import db,Users
import base64


save_img = Blueprint('save_img', __name__, url_prefix='/saveImage')

@save_img.route('/', methods=['GET', 'POST'])
def save_image_db():
    if request.method == 'POST':
        # lấy file ảnh từ form
        image = request.files['image']
        uid=request.form['id']

        # chuyển đổi ảnh thành chuỗi Base64
        base64_image = base64.b64encode(image.read()).decode('utf-8')
        user = Users.query.filter_by(id_user=uid).first()
        if not user:
            return 'User not found'

    # cập nhật ảnh của người dùng
        user.img_avatar = base64_image
        db.session.commit()
        # trả về kết quả và hiển thị trang HTML
        return render_template('saveImage.html', base64_image=base64_image)
    return render_template('saveImage.html')
