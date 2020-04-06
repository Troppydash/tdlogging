import time

from tdlogging.tdlogger import TDLogger

logger = TDLogger(alias="All Logger")

@logger.config()
class Fib:

    def member_method(self):
        pass

    def arguments(self, a, b):
        c = a + b

    def sleep(self, seconds):
        time.sleep(seconds)


Fib().member_method()
Fib().arguments("first arg", "second arg")
Fib().sleep(5)
