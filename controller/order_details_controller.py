from app import app
from model.order_details_model import OrderDetailsModel
from flask import request

obj = OrderDetailsModel()


@app.route('/order-details/getall')
def order_details_getall_controller():
    return obj.order_details_getall_model()

@app.route('/order-details/add', methods=["POST"])
def order_details_addone_controller():
    return obj.order_details_addone_model(request.form)

@app.route('/order-details/update', methods=["POST"])
def order_details_update_controller():
    return obj.order_details_update_model(request.form)

@app.route('/order-details/delete/<fk_order_id>/<fk_playlist_id>', methods=["POST"])
def order_details_delete_controller(fk_order_id, fk_playlist_id):
    return obj.order_details_delete_model(fk_order_id, fk_playlist_id)

@app.route('/order-details/patch/<fk_order_id>/<fk_playlist_id>', methods=["POST"])
def order_details_patch_controller(fk_order_id, fk_playlist_id):
    return obj.order_details_patch_model(request.form, fk_order_id, fk_playlist_id)
