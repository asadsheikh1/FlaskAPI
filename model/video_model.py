import mysql.connector
from flask import make_response
from config.config import dbconfig

class VideoModel():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host=dbconfig['host'], user=dbconfig['user'], password=dbconfig['password'], database=dbconfig['database'])
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print('Connection successful')
        except:
            print('Some error')

    def video_getall_model(self):
        self.cur.execute('SELECT * FROM video')
        result = self.cur.fetchall()
        if len(result) > 0:
            res = make_response({"payload": result}, 200)
            res.headers['Access-Control-Allow-Origin'] = '*'
            return res
        else:
            return make_response({"message": 'No data found'}, 204)

    def video_addone_model(self, data):
        self.cur.execute(f"CALL `course_mania`.`addvideo`('{data['video_name']}', '{data['video_description']}', '{data['added_datetime']}', '{data['thumbnail']}', '{data['video_path']}', {data['fk_playlist_id']})")
        return make_response({"message": 'Video created successfully'}, 201)

    def video_update_model(self, data):
        self.cur.execute(f"UPDATE video SET video_name = '{data['video_name']}', video_description = '{data['video_description']}', added_datetime = '{data['added_datetime']}', thumbnail = '{data['thumbnail']}', video_path = '{data['video_path']}', fk_playlist_id = {data['fk_playlist_id']} WHERE video_id = {data['video_id']}")
        if self.cur.rowcount > 0:
            return make_response({"message": 'Video updated successfully'}, 201)
        else:
            return make_response({"message": 'Nothing to update'}, 202)

    def video_delete_model(self, id):
        self.cur.execute(f"UPDATE video SET is_active = 0 WHERE video_id = {id}")
        if self.cur.rowcount > 0:
            return make_response({"message": 'Video deleted successfully'}, 200)
        else:
            return make_response({"message": 'Nothing to delete'}, 202)
     
    def video_patch_model(self, data, id):
        qry = 'UPDATE video SET '
        for key in data:
            qry += f"{key} = '{data[key]}',"
        qry = qry[:-1] + f' WHERE video_id = {id}'
        
        self.cur.execute(qry)

        if self.cur.rowcount > 0:
            return make_response({"message": 'Video updated successfully'}, 201)
        else:
            return make_response({"message": 'Nothing to update'}, 202)
   
    def video_upload_video_model(self, id, video_path):
        self.cur.execute(f"UPDATE video SET video_path = '{video_path}' WHERE video_id = {id}")
        if self.cur.rowcount > 0:
            return make_response({"message": 'File uploaded successfully'}, 201)
        else:
            return make_response({"message": 'Nothing to update'}, 202)
