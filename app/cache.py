import redis
import json
from config import settings

redis_client = redis.from_url(settings.REDIS_URL)

def set_cache(key: str, value: dict, expires: int = 3600):
    redis_client.setex(key, expires, json.dumps(value))

def get_cache(key: str) -> dict:
    data = redis_client.get(key)
    return json.loads(data) if data else None