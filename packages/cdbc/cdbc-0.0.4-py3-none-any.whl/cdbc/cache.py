
import redis
import json

def redis_connection_pool(redis_host: str, redis_port: int, redis_db: int):
    _pool = redis.ConnectionPool(
        host = redis_host,
        port = redis_port,
        db = redis_db,
        decode_responses = True
    )
    return redis.Redis(connection_pool=_pool)

"""
redis_host = 'dmc-redis-containers.devcloud.geconnect.cn'
redis_port = 16381
redis_db = 1

_pool = redis_connection_pool(redis_host=redis_host, redis_port=redis_port, redis_db=redis_db)


"""

def get_all_kvs(pool):
    _kvs = dict()
    _pool = pool
    _keys = _pool.keys()
    for _k in _keys:
        _kvs[_k] = json.loads(_pool.get(_k))
    return _kvs

"""
redis_host = 'dmc-redis-containers.devcloud.geconnect.cn'
redis_port = 16381
redis_db = 1
_pool = redis_connection_pool(redis_host=redis_host, redis_port=redis_port, redis_db=redis_db)

_kvs = get_all_kvs(pool=_pool)

"""

