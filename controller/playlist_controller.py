from app import app
from model.playlist_model import PlaylistModel
from flask import request, send_file
from datetime import datetime

obj = PlaylistModel()


@app.route('/playlist/getall')
def playlist_getall_controller():
    return obj.playlist_getall_model()

@app.route('/playlist/add', methods=["POST"])
def playlist_addone_controller():
    file = request.files['thumbnail']
    unique_filename = f'{datetime.now().timestamp()}'.replace('.', '')
    filename_split = file.filename.split('.')
    ext = filename_split[len(filename_split) - 1]
    path = f'uploads/thumbnail/{unique_filename}.{ext}'
    file.save(path)
    return obj.playlist_addone_model(request.form, path)

@app.route('/playlist/update', methods=["POST"])
def playlist_update_controller():
    return obj.playlist_update_model(request.form)

@app.route('/playlist/delete/<id>', methods=["POST"])
def playlist_delete_controller(id):
    return obj.playlist_delete_model(id)

@app.route('/playlist/patch/<id>', methods=["POST"])
def playlist_patch_controller(id):
    return obj.playlist_patch_model(request.form, id)

@app.route('/playlist/<id>/upload/thumbnail', methods=["POST"])
def playlist_upload_thumbnail_controller(id):
    file = request.files['thumbnail']
    unique_filename = f'{datetime.now().timestamp()}'.replace('.', '')
    filename_split = file.filename.split('.')
    ext = filename_split[len(filename_split) - 1]
    path = f'uploads/thumbnail/{unique_filename}.{ext}'
    file.save(path)
    return obj.playlist_upload_thumbnail_model(id, path)

@app.route('/uploads/thumbnail/<filename>')
def playlist_get_thumbnail_controller(filename):
    return send_file(f'uploads/thumbnail/{filename}')
