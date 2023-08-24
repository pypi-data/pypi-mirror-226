import redis
import yaml
import json
import psycopg2

class Redis:
    def __init__(self, redis_host=None, redis_port=None, redis_db=None):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.redis_conn = None
    def create_redis_conn(self):
        _pool = redis.ConnectionPool(
                host = self.redis_host,
                port = self.redis_port,
                db = self.redis_db,
                decode_responses = True
            )
        _conn = redis.Redis(connection_pool=_pool)
        self.redis_conn = _conn
    def kvs(self):
        _conn = self.redis_conn
        _kvs = dict()
        _keys = _conn.keys()
        for _k in _keys:
            _v = _conn.get(_k)
            _kvs[_k] = _v
        return _kvs
    def set(self, key:str=None, value:str=None, kvs:dict=None, **kwargs):
        try:
            batch = kwargs['batch']
        except KeyError:
            batch = False
        # batch: bool = False,
        if batch and kvs:
            _conn = self.redis_conn
            for _k in kvs:
                _v = kvs[_k]
                _conn.set(_k, _v)
        else:
            _conn = self.redis_conn
            _conn.set(key, value)
    def get(self, key:str=None):
        if not key:
            return None
        _conn = self.redis_conn
        return _conn.get(key)
