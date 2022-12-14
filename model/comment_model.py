import mysql.connector
from flask import make_response
from config.config import dbconfig

class CommentModel():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host=dbconfig['host'], user=dbconfig['user'], password=dbconfig['password'], database=dbconfig['database'])
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print('Connection successful')
        except:
            print('Some error')

    def comment_getall_model(self):
        self.cur.execute('SELECT * FROM comment')
        result = self.cur.fetchall()
        if len(result) > 0:
            res = make_response({"payload": result}, 200)
            res.headers['Access-Control-Allow-Origin'] = '*'
            return res
        else:
            return make_response({"message": 'No data found'}, 204)

    def comment_addone_model(self, data):
        self.cur.execute(f"CALL `course_mania`.`addcomment`('{data['comment_description']}', '{data['added_datetime']}', {data['fk_user_id']}, {data['fk_video_id']});")
        return make_response({"message": 'Comment created successfully'}, 201)

    def comment_update_model(self, data):
        self.cur.execute(f"UPDATE comment SET comment_description = '{data['comment_description']}', added_datetime = '{data['added_datetime']}', fk_user_id = {data['fk_user_id']}, fk_video_id = {data['fk_video_id']} WHERE comment_id = {data['comment_id']};")
        if self.cur.rowcount > 0:
            return make_response({"message": 'Comment updated successfully'}, 201)
        else:
            return make_response({"message": 'Nothing to update'}, 202)

    def comment_delete_model(self, id):
        self.cur.execute(f"UPDATE comment SET is_active = 0 WHERE comment_id = {id}")
        if self.cur.rowcount > 0:
            return make_response({"message": 'Comment deleted successfully'}, 200)
        else:
            return make_response({"message": 'Nothing to delete'}, 202)
     
    def comment_patch_model(self, data, id):
        qry = 'UPDATE comment SET '
        for key in data:
            qry += f"{key} = '{data[key]}',"
        qry = qry[:-1] + f' WHERE comment_id = {id}'
        
        self.cur.execute(qry)

        if self.cur.rowcount > 0:
            return make_response({"message": 'Comment updated successfully'}, 201)
        else:
            return make_response({"message": 'Nothing to update'}, 202)
