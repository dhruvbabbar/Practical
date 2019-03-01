import pymysql.cursors

class MySQLConnection:
    def __init__(self,dbconfig:dict):
        self.configuration = dbconfig
        
    def __enter__(self):
        try:
            self.conn = pymysql.connect(**self.configuration)
            self.cursor = self.conn.cursor()
            return self.cursor
        except Exception as err:
            print("Could not connect to the database. Error is :"+str(err))
        except OperationalError as operr:
            print(str(operr))
    def __exit__(self,exc_type,exc_value,exc_trace):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        