
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


def redis_get_kvs(pool):
    _kvs = dict()
    _pool = pool
    _keys = _pool.keys()
    for _k in _keys:
        _kvs[_k] = json.loads(_pool.get(_k))
    return _kvs
