import pyodbc
from config import db


class Odbc(object):
    def __init__(self):
        self.dsn = db['dsn']
        self.username = db['username']
        self.password = db['password']
        self.connect()

    def connect(self):
        connection_string = "DATABASE=%s; UID=%s; PASSWORD=%s" % (self.dsn, self.username, self.password)
        self.conn = pyodbc.connect(connection_string)
        return True

    def select_row_array(self, sql):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
        except:
            raise
        result = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        cursor.close()
        return result, columns
