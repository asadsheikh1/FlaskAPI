import mysql.connector
from flask import make_response
from config.config import dbconfig

class OrderDetailsModel():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host=dbconfig['host'], user=dbconfig['user'], password=dbconfig['password'], database=dbconfig['database'])
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print('Connection successful')
        except:
            print('Some error')

    def order_details_getall_model(self):
        self.cur.execute('SELECT * FROM order_details;')
        result = self.cur.fetchall()
        if len(result) > 0:
            res = make_response({"payload": result}, 200)
            res.headers['Access-Control-Allow-Origin'] = '*'
            return res
        else:
            return make_response({"message": 'No data found'}, 204)

    def order_details_addone_model(self, data):
        self.cur.execute(f"CALL `course_mania`.`addorderdetails`('{data['fk_order_id']}', '{data['fk_playlist_id']}', '{data['added_datetime']}');")
        return make_response({"message": 'Order Details added successfully'}, 201)

    def order_details_update_model(self, data):
        self.cur.execute(f"UPDATE order_details SET fk_order_id = '{data['order_id']}', fk_playlist_id = '{data['playlist_id']}', added_datetime = '{data['added_datetime']}' WHERE fk_order_id = {data['fk_order_id']} AND fk_playlist_id = {data['fk_playlist_id']};")
        if self.cur.rowcount > 0:
            return make_response({"message": 'Order Details updated successfully'}, 201)
        else:
            return make_response({"message": 'Nothing to update'}, 202)

    def order_details_delete_model(self, fk_order_id, fk_playlist_id):
        self.cur.execute(f"UPDATE order_details SET is_active = 0 WHERE fk_order_id = {fk_order_id} AND fk_playlist_id = {fk_playlist_id}")
        if self.cur.rowcount > 0:
            return make_response({"message": 'Order Details deleted successfully'}, 200)
        else:
            return make_response({"message": 'Nothing to delete'}, 202)
     
    def order_details_patch_model(self, data, fk_order_id, fk_playlist_id):
        qry = 'UPDATE order_details SET '
        for key in data:
            qry += f"{key} = {data[key]},"
        qry = qry[:-1] + f' WHERE fk_order_id = {fk_order_id} AND fk_playlist_id = {fk_playlist_id}'
        
        self.cur.execute(qry)

        if self.cur.rowcount > 0:
            return make_response({"message": 'Order Details updated successfully'}, 201)
        else:
            return make_response({"message": 'Nothing to update'}, 202)
