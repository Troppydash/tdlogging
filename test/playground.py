from tdlogging.tdlogger import TDLogger

logger = TDLogger(alias="Sleep Logger")


@logger.config()
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


print(Fib.get_n(5))