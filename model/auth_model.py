from functools import wraps
import mysql.connector
from flask import make_response, request
from config.config import dbconfig
import json
import jwt
import re

class AuthModel():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host=dbconfig['host'], user=dbconfig['user'], password=dbconfig['password'], database=dbconfig['database'])
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print('Connection successful')
        except:
            print('Some error')

    def token_auth(self, endpoint=""):
        def inner1(func):
            @wraps(func)
            def inner2(*args):
                endpoint = request.url_rule
                authorization = request.headers.get("authorization")
                if re.match("^Bearer *([^ ]+) *$", authorization, flags=0):
                    token = authorization.split(" ")[1]
                    try:
                        jwt_decoded = jwt.decode(token, "asad", algorithms="HS256")
                    except jwt.ExpiredSignatureError:
                        return make_response({"ERROR": "TOKEN_EXPIRED"}, 401)

                    fk_role_id = jwt_decoded['payload']['fk_role_id']
                    self.cur.execute(f"SELECT roles FROM accessibility_view WHERE endpoint_name = '{endpoint}'")
                    result = self.cur.fetchall()

                    if len(result) > 0:
                        allowed_roles = json.loads(result[0]['roles'])
                        if fk_role_id in allowed_roles:
                            return func(*args)
                        else:
                            return make_response({"ERROR": "INVALID_ROLE"}, 404)

                    else:
                        return make_response({"ERROR": "UNKNOWN_ENDPOINT"}, 404)

                else:
                    return make_response({"ERROR": "INVALID_TOKEN"}, 401)
            return inner2
        return inner1
