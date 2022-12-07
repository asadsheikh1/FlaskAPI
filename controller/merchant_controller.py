from app import app
from model.merchant_model import MerchantModel
from flask import request

obj = MerchantModel()


@app.route('/merchant/getall')
def merchant_getall_controller():
    return obj.merchant_getall_model()

@app.route('/merchant/add', methods=["POST"])
def merchant_addone_controller():
    return obj.merchant_addone_model(request.form)

@app.route('/merchant/update', methods=["POST"])
def merchant_update_controller():
    return obj.merchant_update_model(request.form)

@app.route('/merchant/delete/<id>', methods=["POST"])
def merchant_delete_controller(id):
    return obj.merchant_delete_model(id)

@app.route('/merchant/patch/<id>', methods=["POST"])
def merchant_patch_controller(id):
    return obj.merchant_patch_model(request.form, id)
