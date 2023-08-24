import psycopg2
import json
from psycopg2 import pool


class PG:
    def __init__(self, host:str=None, port:int=None, database:str=None, user:str=None, password:str=None):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.pg_conn = None
        self.pg_pool = None
    def create_pg_conn(self):
        _pg_connect = psycopg2.connect(
            host = self.host,
            database = self.database,
            port = self.port,
            user = self.user,
            password = self.password
        )
        self.pg_conn = _pg_connect
    def create_pg_pool(self):
        _pg_pool = psycopg2.pool.SimpleConnectionPool(
            1,  # minimum number of connections
        10,  # maximum number of connections
        user = self.user,
        password = self.password,
        host = self.host,
        port = self.port,
        database = self.database
    )
        self.pg_pool = _pg_pool.getconn()
    def select(self, sql):
        try:
            _cursor = self.pg_conn.cursor()
            _cursor.execute(sql)
            results = _cursor.fetchall()
            _cursor.close()
            return results
        except Exception as e:
            return e
    def select_from_pool(self, sql):
        try:
            _cursor = self.pg_pool.cursor()
            _cursor.execute(sql)
            results = _cursor.fetchall()
            _cursor.close()
            return results
        except Exception as e:
            return e
    def insert(self, table:str, cvs:list):
        try:
            _cursor = self.pg_conn.cursor()
            _cursor.execute("INSERT INTO {0}({1}) VALUES({2})".format(table, cvs[0], cvs[1]))
            self.pg_conn.commit()
            _cursor.close()
            # conn.close()
            return {
                'rc': 200,
                'cur_result': 'successful'
            }
        except Exception as e:
            return {
                'rc': 500,
                'cur_result': e
            }
    def insert_with_pool(self, table:str, cvs:list):
        try:
            _cursor = self.pg_pool.cursor()
            _cursor.execute("INSERT INTO {0}({1}) VALUES({2})".format(table, cvs[0], cvs[1]))
            self.pg_pool.commit()
            _cursor.close()
            # conn.close()
            return {
                'rc': 200,
                'cur_result': 'successful'
            }
        except Exception as e:
            return {
                'rc': 500,
                'cur_result': e
            }
    def orm_select(self):
        pass
    def orm_insert(self):
        pass




