import psycopg2
import json

def conn(host:str, port: int, database:str, user: str, password:str):
    _db_connect = psycopg2.connect(
        host=host,
        database=database,
        port = port,
        user=user,
        password=password
    )
    return _db_connect

"""
host = '10.191.101.139'
database = 'backbone-manager'
port = 5432
user = 'backbone-manager-user'
password = 'backbone-manager-paSSw0rd'
_conn = conn(host=host, port=port, database=database, user=user, password=password)
"""


def select(cursor, sql):
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results
    except Exception as e:
        return e

"""

n = 1
while n < 200:
    sql = 'select count(*) from rtt'
    _conn = conn(host=host, port=port, database=database, user=user, password=password)
    _cursor = _conn.cursor()
    select(cursor=_cursor,sql=sql)
    n = n + 1
    time.sleep(1)
"""


def insert(conn, table:str, cvs:list):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO {0}({1}) VALUES({2})".format(table, cvs[0], cvs[1]))
        conn.commit()
        cursor.close()
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


columns = 'col1, col2, col3'
values = "'" + 'value1' + "'" + ', '\
         + "'" + 'value2' + "'" + ', '\
         + "'" + json.dumps({'k':'v'}) + "'"
cvs = [columns, values]



host = '10.191.101.139'
database = 'backbone-manager'
port = 5432
user = 'backbone-manager-user'
password = 'backbone-manager-paSSw0rd'
_conn = conn(host=host, port=port, database=database, user=user, password=password)

_conn = conn(host=host, port=port, database=database, user=user, password=password)
_cursor = _conn.cursor()

"""
import random
import string

_conn = conn(host=host, port=port, database=database, user=user, password=password)

table = 'sample'
columns = 'col1, col2, col3'

n = 1
while n < 10000:
    value1 = ''.join([random.choice(string.ascii_lowercase + string.digits) for _n in range(10)])
    value2 = ''.join([random.choice(string.ascii_lowercase + string.digits) for _n in range(10)])
    k = ''.join([random.choice(string.ascii_lowercase + string.digits) for _n in range(5)])
    v = ''.join([random.choice(string.ascii_lowercase + string.digits) for _n in range(5)])
    values = "'" + value1 + "'" + ', '\
         + "'" + value2 + "'" + ', '\
         + "'" + json.dumps({k:v}) + "'"
    cvs = [columns, values]
    insert(conn=_conn, table=table, cvs=cvs)
    n = n + 1

"""
