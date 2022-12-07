from app import app
from model.user_model import UserModel
from flask import request, send_file
from datetime import datetime

obj = UserModel()


@app.route('/user/getall')
def user_getall_controller():
    return obj.user_getall_model()

@app.route('/user/add', methods=["POST"])
def user_add_controller():
    return obj.user_add_model(request.form)

@app.route('/user/update', methods=["POST"])
def user_update_controller():
    return obj.user_update_model(request.form)

@app.route('/user/delete/<id>', methods=["POST"])
def user_delete_controller(id):
    return obj.user_delete_model(id)

@app.route('/user/patch/<id>', methods=["POST"])
def user_patch_controller(id):
    return obj.user_patch_model(request.form, id)

@app.route('/user/<id>/upload/avatar', methods=["POST"])
def user_upload_avatar_controller(id):
    file = request.files['avatar']
    unique_filename = f'{datetime.now().timestamp()}'.replace('.', '')
    filename_split = file.filename.split('.')
    ext = filename_split[len(filename_split) - 1]
    path = f'uploads/avatar/{unique_filename}.{ext}'
    file.save(path)
    return obj.user_upload_avatar_model(id, path)

@app.route('/uploads/avatar/<filename>')
def user_get_avatar_controller(filename):
    return send_file(f'uploads/avatar/{filename}')
 