from app import app
from model.category_model import CategoryModel
from flask import request

obj = CategoryModel()


@app.route('/category/getall')
def category_getall_controller():
    return obj.category_getall_model()

@app.route('/category/add', methods=["POST"])
def category_addone_controller():
    return obj.category_addone_model(request.form)

@app.route('/category/update', methods=["POST"])
def category_update_controller():
    return obj.category_update_model(request.form)

@app.route('/category/delete/<id>', methods=["POST"])
def category_delete_controller(id):
    return obj.category_delete_model(id)

@app.route('/category/patch/<id>', methods=["POST"])
def category_patch_controller(id):
    return obj.category_patch_model(request.form, id)
