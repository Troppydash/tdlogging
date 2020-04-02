import time

from tdlogging.tdlogger import create_logger

logger = create_logger()


@logger.get_logger()
class Fib:

    @staticmethod
    def do_nothing(lmao):
        pass

    @staticmethod
    def get_n(n):
        a = 0
        b = 1

        if n == 0:
            return a
        elif n == 1:
            return b
        else:
            for i in range(2, n):
                c = a + b
                a = b
                b = c
            return b

    @staticmethod
    def sleep(seconds):
        time.sleep(seconds)


while True:
    Fib.sleep(1)
