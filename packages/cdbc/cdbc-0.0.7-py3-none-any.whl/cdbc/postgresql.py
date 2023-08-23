import psycopg2

def conn(host:str, port: int, database:str, user: str, password:str):
    _db_connect = psycopg2.connect(
        host=host,
        database=database,
        port = port,
        user=user,
        password=password
    )
    return _db_connect


def select(cursor, sql):
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results
    except Exception as e:
        return e


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

