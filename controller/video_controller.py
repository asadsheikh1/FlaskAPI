from app import app
from model.video_model import VideoModel
from flask import request, send_file
from datetime import datetime

obj = VideoModel()


@app.route('/video/getall')
def video_getall_controller():
    return obj.video_getall_model()

@app.route('/video/add', methods=["POST"])
def video_addone_controller():
    return obj.video_addone_model(request.form)

@app.route('/video/update', methods=["POST"])
def video_update_controller():
    return obj.video_update_model(request.form)

@app.route('/video/delete/<id>', methods=["POST"])
def video_delete_controller(id):
    return obj.video_delete_model(id)

@app.route('/video/patch/<id>', methods=["POST"])
def video_patch_controller(id):
    return obj.video_patch_model(request.form, id)

@app.route('/video/<id>/upload/video', methods=["POST"])
def video_upload_video_controller(id):
    file = request.files['video_path']
    unique_filename = f'{datetime.now().timestamp()}'.replace('.', '')
    filename_split = file.filename.split('.')
    ext = filename_split[len(filename_split) - 1]
    video_path = f'uploads/video/{unique_filename}.{ext}'
    file.save(video_path)
    return obj.video_upload_video_model(id, video_path)

@app.route('/uploads/video/<filename>')
def video_get_video_controller(filename):
    return send_file(f'uploads/video/{filename}')
 