from app import app
from model.order_model import OrderModel
from flask import request

obj = OrderModel()


@app.route('/order/getall')
def order_getall_controller():
    return obj.order_getall_model()

@app.route('/order/add', methods=["POST"])
def order_addone_controller():
    return obj.order_addone_model(request.form)

@app.route('/order/update', methods=["POST"])
def order_update_controller():
    return obj.order_update_model(request.form)

@app.route('/order/delete/<id>', methods=["POST"])
def order_delete_controller(id):
    return obj.order_delete_model(id)

@app.route('/order/patch/<id>', methods=["POST"])
def order_patch_controller(id):
    return obj.order_patch_model(request.form, id)
