import mysql.connector
from flask import make_response
from config.config import dbconfig

class UserModel():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host=dbconfig['host'], user=dbconfig['user'], password=dbconfig['password'], database=dbconfig['database'])
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print('Connection successful')
        except:
            print('Some error')

    def user_getall_model(self):
        self.cur.execute('SELECT * FROM user')
        result = self.cur.fetchall()
        if len(result) > 0:
            res = make_response({"payload": result}, 200)
            res.headers['Access-Control-Allow-Origin'] = '*'
            return res
        else:
            return make_response({"message": 'No data found'}, 204)

    def user_add_model(self, data):
        self.cur.execute(f"CALL `course_mania`.`adduser`('{data['user_name']}', '{data['email']}', '{data['phone']}', '{data['user_password']}')")
        return make_response({"message": 'User created successfully'}, 201)

    def user_update_model(self, data):
        self.cur.execute(f"UPDATE user SET user_name = '{data['user_name']}', email = '{data['email']}', dob = '{data['dob']}', location = '{data['location']}', phone = '{data['phone']}', user_password = '{data['user_password']}', subscriber_count = '{data['subscriber_count']}' WHERE user_id = {data['user_id']}")
        if self.cur.rowcount > 0:
            return make_response({"message": 'User updated successfully'}, 201)
        else:
            return make_response({"message": 'Nothing to update'}, 202)

    def user_delete_model(self, id):
        self.cur.execute(f"UPDATE user SET is_active = 0 WHERE user_id = {id}")
        if self.cur.rowcount > 0:
            return make_response({"message": 'User deleted successfully'}, 200)
        else:
            return make_response({"message": 'Nothing to delete'}, 202)
     
    def user_patch_model(self, data, id):
        qry = 'UPDATE user SET '
        for key in data:
            qry += f"{key} = '{data[key]}',"
        qry = qry[:-1] + f' WHERE user_id = {id}'
        self.cur.execute(qry)
        if self.cur.rowcount > 0:
            return make_response({"message": 'User updated successfully'}, 201)
        else:
            return make_response({"message": 'Nothing to update'}, 202)

    def user_upload_avatar_model(self, id, path):
        self.cur.execute(f"UPDATE user SET avatar = '{path}' WHERE user_id = {id}")
        if self.cur.rowcount > 0:
            return make_response({"message": 'File uploaded successfully'}, 201)
        else:
            return make_response({"message": 'Nothing to update'}, 202)
