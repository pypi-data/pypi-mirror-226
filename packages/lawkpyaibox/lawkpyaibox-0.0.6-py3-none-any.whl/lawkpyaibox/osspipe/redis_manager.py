import redis
import time
import ast


class RedisManager():

    def __init__(self,
                 redis_identity,
                 redis_host="",
                 redis_port=6379,
                 redis_pwd="",
                 redis_timeout=None):
        self.redis_identity = redis_identity
        self.redis_timeout = redis_timeout
        self.redis_agent = redis.StrictRedis(host=redis_host,
                                             port=redis_port,
                                             password=redis_pwd)

    def redis_get_data(self, keyid):
        # keyid = self.redis_identity + "-" + keyid
        redisvalue = self.redis_agent.get(keyid)
        if redisvalue is None:
            return None
        redisvalue = ast.literal_eval(redisvalue.decode('utf-8'))
        return redisvalue

    def redis_write_datas(self, inputs: dict):
        if self.redis_agent is None:
            return False

        if self.redis_timeout is None:
            for key in inputs.keys():
                # keyid = self.redis_identity + "-" + key
                self.redis_agent.set(key, str(inputs[key]))
        else:
            for key in inputs.keys():
                # keyid = self.redis_identity + "-" + key
                self.redis_agent.set(key,
                                     str(inputs[key]),
                                     ex=self.redis_timeout)
        return True

    def redis_write_data(self, keyid, value):
        if self.redis_agent is None:
            return False
        # keyid = self.redis_identity + "-" + keyid
        if self.redis_timeout is None:
            self.redis_agent.set(keyid, str(value))
        else:
            self.redis_agent.set(keyid, str(value), ex=self.redis_timeout)
        return True
