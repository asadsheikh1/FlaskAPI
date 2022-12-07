import mysql.connector
from flask import make_response
from config.config import dbconfig

class MerchantModel():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host=dbconfig['host'], user=dbconfig['user'], password=dbconfig['password'], database=dbconfig['database'])
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print('Connection successful')
        except:
            print('Some error')

    def merchant_getall_model(self):
        self.cur.execute('SELECT * FROM merchant')
        result = self.cur.fetchall()
        if len(result) > 0:
            res = make_response({"payload": result}, 200)
            res.headers['Access-Control-Allow-Origin'] = '*'
            return res
        else:
            return make_response({"message": 'No data found'}, 204)

    def merchant_addone_model(self, data):
        self.cur.execute(f"CALL `course_mania`.`addmerchant`('{data['merchant_name']}', '{data['account_number']}', '{data['branch_code']}', '{data['iban']}', {data['fk_user_id']});")
        return make_response({"message": 'Merchant created successfully'}, 201)

    def merchant_update_model(self, data):
        self.cur.execute(f"UPDATE merchant SET merchant_name = '{data['merchant_name']}', account_number = '{data['account_number']}', branch_code = '{data['branch_code']}', iban = '{data['iban']}', fk_user_id = {data['fk_user_id']} WHERE merchant_id = {data['merchant_id']};")
        if self.cur.rowcount > 0:
            return make_response({"message": 'Merchant updated successfully'}, 201)
        else:
            return make_response({"message": 'Nothing to update'}, 202)

    def merchant_delete_model(self, id):
        self.cur.execute(f"UPDATE merchant SET is_active = 0 WHERE merchant_id = {id}")
        if self.cur.rowcount > 0:
            return make_response({"message": 'Merchant deleted successfully'}, 200)
        else:
            return make_response({"message": 'Nothing to delete'}, 202)
     
    def merchant_patch_model(self, data, id):
        qry = 'UPDATE merchant SET '
        for key in data:
            qry += f"{key} = {data[key]},"
        qry = qry[:-1] + f' WHERE merchant_id = {id}'
        
        self.cur.execute(qry)

        if self.cur.rowcount > 0:
            return make_response({"message": 'Merchant updated successfully'}, 201)
        else:
            return make_response({"message": 'Nothing to update'}, 202)
