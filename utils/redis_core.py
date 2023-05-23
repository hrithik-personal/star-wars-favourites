import redis
import json


# Create a Redis connection
redis_connection = redis.Redis(host='localhost', port=6379, db=0)


def cache_get(key):
    """
    Retrieve data from Redis cache based on the given key.
    """
    data = redis_connection.get(key)
    if data:
        return json.loads(data)
    return None


def cache_set(key, data, ttl=None):
    """
    Store data in Redis cache with the given key and optional time-to-live (TTL).
    """
    if not isinstance(data, (str, bytes)):
        data = json.dumps(data)
    redis_connection.set(key, data)
    if ttl:
        redis_connection.expire(key, ttl)
