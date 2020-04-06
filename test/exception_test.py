from tdlogging.tdlogger import TDLogger

logger = TDLogger(alias="Exception Logger")


@logger.config()
class Fib:

    @staticmethod
    def bad_method():
        raise Exception("Hello")


Fib.bad_method()
