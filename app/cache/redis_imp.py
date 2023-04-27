from settings import settings
from redis import Redis

redis = Redis(host=settings.redis_host, port=settings.redis_port, password=settings.redis_password, decode_responses=True)