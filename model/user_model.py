import mysql.connector
from flask import make_response
from config.config import dbconfig
from datetime import datetime, timedelta
import jwt

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

    def user_login_model(self, data):
        self.cur.execute(f"SELECT user_id, user_name, email, dob, location, phone, avatar, subscriber_count, fk_role_id, is_active FROM user WHERE email = '{data['email']}' and user_password = '{data['user_password']}'")
        result = self.cur.fetchall()
        user_data = result[0]
        user_id = user_data['user_id']
        user_name = user_data['user_name']
        email = user_data['email']
        dob = user_data['dob']
        location = user_data['location']
        phone = user_data['phone']
        avatar = user_data['avatar']
        subscriber_count = user_data['subscriber_count']
        fk_role_id = user_data['fk_role_id']
        exp_time = datetime.now() + timedelta(minutes=15)
        exp_epoch_time = int(exp_time.timestamp())
        payload = {
            "payload": user_data,
            "exp": exp_epoch_time,
        }
        jwtoken = jwt.encode(payload, "asad", algorithm="HS256")
        return make_response({"user_id": user_id, "user_name": user_name, "email": email, "dob": dob, "location": location, "phone": phone, "avatar": avatar, "subscriber_count": subscriber_count, "fk_role_id": fk_role_id, "token": jwtoken}, 200)
