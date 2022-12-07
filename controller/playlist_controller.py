from app import app
from model.playlist_model import PlaylistModel
from flask import request

obj = PlaylistModel()


@app.route('/playlist/getall')
def playlist_getall_controller():
    return obj.playlist_getall_model()

@app.route('/playlist/add', methods=["POST"])
def playlist_addone_controller():
    return obj.playlist_addone_model(request.form)

@app.route('/playlist/update', methods=["POST"])
def playlist_update_controller():
    return obj.playlist_update_model(request.form)

@app.route('/playlist/delete/<id>', methods=["POST"])
def playlist_delete_controller(id):
    return obj.playlist_delete_model(id)

@app.route('/playlist/patch/<id>', methods=["POST"])
def playlist_patch_controller(id):
    return obj.playlist_patch_model(request.form, id)
