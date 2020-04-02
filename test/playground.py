from tdlogging.tdlogger import create_logger

logger = create_logger()


@logger.get_logger()
class Fib:
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


Fib.get_n(9)
