import mysql.connector
from flask import make_response
from config.config import dbconfig

class CategoryModel():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host=dbconfig['host'], user=dbconfig['user'], password=dbconfig['password'], database=dbconfig['database'])
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print('Connection successful')
        except:
            print('Some error')

    def category_getall_model(self):
        self.cur.execute('SELECT * FROM category')
        result = self.cur.fetchall()
        if len(result) > 0:
            res = make_response({"payload": result}, 200)
            res.headers['Access-Control-Allow-Origin'] = '*'
            return res
        else:
            return make_response({"message": 'No data found'}, 204)

    def category_addone_model(self, data):
        self.cur.execute(f"CALL `course_mania`.`addcategory`('{data['category_name']}');")
        return make_response({"message": 'Category created successfully'}, 201)

    def category_update_model(self, data):
        self.cur.execute(f"UPDATE category SET category_name = '{data['category_name']}' WHERE category_id = {data['category_id']}")
        if self.cur.rowcount > 0:
            return make_response({"message": 'Category updated successfully'}, 201)
        else:
            return make_response({"message": 'Nothing to update'}, 202)

    def category_delete_model(self, id):
        self.cur.execute(f"UPDATE category SET is_active = 0 WHERE category_id = {id}")
        if self.cur.rowcount > 0:
            return make_response({"message": 'Category deleted successfully'}, 200)
        else:
            return make_response({"message": 'Nothing to delete'}, 202)
     
    def category_patch_model(self, data, id):
        qry = 'UPDATE category SET '
        for key in data:
            qry += f"{key} = '{data[key]}',"
        qry = qry[:-1] + f' WHERE category_id = {id}'
        
        self.cur.execute(qry)

        if self.cur.rowcount > 0:
            return make_response({"message": 'Category updated successfully'}, 201)
        else:
            return make_response({"message": 'Nothing to update'}, 202)
