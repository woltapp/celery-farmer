import redis


class Broker:
    def get_queue_length(self, queue):
        raise NotImplementedError(
            'Subclass needs to implement get_queue_length')


class RedisBroker(Broker):
    def __init__(self, redis_uri):
        self.client = redis.StrictRedis.from_url(redis_uri)

    def get_queue_length(self, queue):
        return self.client.llen(queue)
