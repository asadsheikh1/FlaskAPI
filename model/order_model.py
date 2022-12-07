import mysql.connector
from flask import make_response
from config.config import dbconfig

class OrderModel():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host=dbconfig['host'], user=dbconfig['user'], password=dbconfig['password'], database=dbconfig['database'])
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print('Connection successful')
        except:
            print('Some error')

    def order_getall_model(self):
        self.cur.execute('SELECT * FROM `order`')
        result = self.cur.fetchall()
        if len(result) > 0:
            res = make_response({"payload": result}, 200)
            res.headers['Access-Control-Allow-Origin'] = '*'
            return res
        else:
            return make_response({"message": 'No data found'}, 204)

    def order_addone_model(self, data):
        self.cur.execute(f"CALL `course_mania`.`addorder`();")
        return make_response({"message": 'Order created successfully'}, 201)

    def order_update_model(self, data):
        self.cur.execute(f"UPDATE `order` SET is_active = {data['is_active']} WHERE order_id = {data['order_id']}")
        if self.cur.rowcount > 0:
            return make_response({"message": 'Order updated successfully'}, 201)
        else:
            return make_response({"message": 'Nothing to update'}, 202)

    def order_delete_model(self, id):
        self.cur.execute(f"UPDATE `order` SET is_active = 0 WHERE order_id = {id}")
        if self.cur.rowcount > 0:
            return make_response({"message": 'Order deleted successfully'}, 200)
        else:
            return make_response({"message": 'Nothing to delete'}, 202)
     
    def order_patch_model(self, data, id):
        qry = 'UPDATE `order` SET '
        for key in data:
            qry += f"{key} = '{data[key]}',"
        qry = qry[:-1] + f' WHERE order_id = {id}'
        
        self.cur.execute(qry)

        if self.cur.rowcount > 0:
            return make_response({"message": 'Order updated successfully'}, 201)
        else:
            return make_response({"message": 'Nothing to update'}, 202)
