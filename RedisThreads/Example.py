import time

from redis import Redis
from redis.client import PubSubWorkerThread
from redis.exceptions import ConnectionError as RedisConnError


class Redis_On_Thread_Exc(Exception):
    pass


class Redis_On_Thread:
    __HOST: str  = "127.0.0.1"
    __PORT: int  = 6379
    __TOPIC: str = "TOPIC_NAME"

    def __init__(self):
        try:
            self.__redis_message_handler = None
            # make connection
            # decode_responses=True will trim special chars like ascii 10 | 13 aka \n \r
            self.__redis = Redis(host=self.__HOST, port=self.__PORT, decode_responses=True)
            # flush db
            self.__redis.flushall()
            # get a pubsub
            self.__pubsub = self.__redis.pubsub()
            # attach pubsub instance to thread scope
            self.__pubsub.psubscribe(**{self.__TOPIC: self.__on_message})

            # you can attach more than one thread
            # self.__pubsub.psubscribe(**{"OTHER_TOPIC_NAME": self.__other_function})
        except RedisConnError or OSError or ConnectionRefusedError:
            raise Redis_On_Thread_Exc(f'Unable to connect to redis server at: {self.__HOST}:{self.__PORT}')

        # sleep_time disable CPU burning :)
        # detach threads
        self.__redis_message_handler: PubSubWorkerThread = self.__pubsub.run_in_thread(sleep_time=0.01)

    def stop(self) -> None:
        self.__redis_message_handler.stop()
        self.__redis.close()

    def __on_message(self, msg) -> None:
        """
        thread body
        here you will receive msg published on self.__TOPIC
        """
        _key = msg['data']
        _message = self.__redis.get(_key)

        # do what you want with this msg
        print(_message)

    def push_msg(self, topic, key, msg) -> None:
        # assoc key -> msg
        # msg can be str | json | basic types
        self.__redis.set(key, msg)

        # pub topic -> key
        self.__redis.publish(topic, key)

    def dummy_function(self) -> None:
        """
        Need help?
        """
        while True:
            time.sleep(1)


if __name__ == "__main__":
    try:
        obj: Redis_On_Thread = Redis_On_Thread()
        obj.begin()
        obj.dummy_function()
    except Redis_On_Thread_Exc as rexc:
        print(rexc.args)
    except KeyboardInterrupt:
        pass








