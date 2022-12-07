from app import app
from model.comment_model import CommentModel
from flask import request

obj = CommentModel()


@app.route('/comment/getall')
def comment_getall_controller():
    return obj.comment_getall_model()

@app.route('/comment/add', methods=["POST"])
def comment_addone_controller():
    return obj.comment_addone_model(request.form)

@app.route('/comment/update', methods=["POST"])
def comment_update_controller():
    return obj.comment_update_model(request.form)

@app.route('/comment/delete/<id>', methods=["POST"])
def comment_delete_controller(id):
    return obj.comment_delete_model(id)

@app.route('/comment/patch/<id>', methods=["POST"])
def comment_patch_controller(id):
    return obj.comment_patch_model(request.form, id)
