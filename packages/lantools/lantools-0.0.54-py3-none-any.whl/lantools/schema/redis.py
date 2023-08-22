from typing import Any
from pydantic import BaseModel
from redis import StrictRedis


class Redis(BaseModel):
    host: str
    port: int = 6379
    db: int = 0
    username: str = None
    password: str = None

    redis: Any = None
    cache: Any = None

    def get_dsn(self):
        if self.username!=None and self.password!=None:
            return 'redis://{}:{}@{}:{}/{}'.format(self.username, self.password, self.host, self.port, self.db)
        else:
            return 'redis://{}:{}/{}'.format(self.host, self.port, self.db)

    def connect(self) -> StrictRedis:
        self.redis = StrictRedis(host=self.host, port=self.port, username=self.username, password=self.password, db=self.db, decode_responses=True)
        return self.redis

    def instance(self) -> StrictRedis:
        if self.redis==None:
            self.redis = self.connect()
            return self.redis
        else:
            try:
                self.redis.ping()
                return self.redis
            except Exception as e:
                self.redis = self.connect()
                return self.redis

    def llen(self, queue):
        try:
            return self.redis.llen(queue)
        except Exception:
            return self.connect().llen(queue)

    def lpush(self, queue, value):
        try:
            return self.redis.lpush(queue, value)
        except Exception:
            return self.connect().lpush(queue, value)

    def rpop(self, queue):
        try:
            return self.redis.rpop(queue)
        except Exception:
            return self.connect().rpop(queue)

    def cache_it(self, *, limit=100000, expire=3600, hashkeys=True, namespace="default"):
        if self.cache==None:
            from redis_cache import SimpleCache,cache_it
            my_cache = SimpleCache(limit=limit, expire=expire, hashkeys=hashkeys, host=self.host, port=self.port, db=self.db, namespace=namespace)
            self.cache = cache_it(cache=my_cache)
        return self.cache

