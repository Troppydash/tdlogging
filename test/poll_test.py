import time

from tdlogging.tdlogger import TDLogger

logger = TDLogger(alias="Sleep Logger")


@logger.config()
class Fib:

    def sleep(self, seconds):
        time.sleep(seconds)


while True:
    Fib().sleep(1)
