import mysql.connector
from flask import make_response
from config.config import dbconfig

class PlaylistModel():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host=dbconfig['host'], user=dbconfig['user'], password=dbconfig['password'], database=dbconfig['database'])
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print('Connection successful')
        except:
            print('Some error')

    def playlist_getall_model(self):
        self.cur.execute('SELECT playlist_id, playlist_name, playlist_description, cast(cost as char(13)) cost, cast(rating as char(3)) rating, fk_category_id, fk_user_id, fk_merchant_id, is_active FROM playlist')
        result = self.cur.fetchall()
        if len(result) > 0:
            res = make_response({"payload": result}, 200)
            res.headers['Access-Control-Allow-Origin'] = '*'
            return res
        else:
            return make_response({"message": 'No data found'}, 204)

    def playlist_addone_model(self, data):
        self.cur.execute(f"CALL `course_mania`.`addplaylist`('{data['playlist_name']}', '{data['playlist_description']}', '{data['cost']}', '{data['rating']}', {data['fk_category_id']}, {data['fk_user_id']}, {data['fk_merchant_id']});")
        return make_response({"message": 'Playlist created successfully'}, 201)

    def playlist_update_model(self, data):
        self.cur.execute(f"UPDATE playlist SET playlist_name = '{data['playlist_name']}', playlist_description = '{data['playlist_description']}', cost = '{data['cost']}', rating = '{data['rating']}', fk_category_id = '{data['fk_category_id']}', fk_user_id = '{data['fk_user_id']}', fk_merchant_id = '{data['fk_merchant_id']}' WHERE playlist_id = {data['playlist_id']}")
        if self.cur.rowcount > 0:
            return make_response({"message": 'Playlist updated successfully'}, 201)
        else:
            return make_response({"message": 'Nothing to update'}, 202)

    def playlist_delete_model(self, id):
        self.cur.execute(f"UPDATE playlist SET is_active = 0 WHERE playlist_id = {id}")
        if self.cur.rowcount > 0:
            return make_response({"message": 'Playlist deleted successfully'}, 200)
        else:
            return make_response({"message": 'Nothing to delete'}, 202)
     
    def playlist_patch_model(self, data, id):
        qry = 'UPDATE playlist SET '
        for key in data:
            qry += f"{key} = '{data[key]}',"
        qry = qry[:-1] + f' WHERE playlist_id = {id}'
        
        self.cur.execute(qry)

        if self.cur.rowcount > 0:
            return make_response({"message": 'Playlist updated successfully'}, 201)
        else:
            return make_response({"message": 'Nothing to update'}, 202)
