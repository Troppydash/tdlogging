from tdlogging.tdlogger import TDLogger
from tdlogging.tdprinter import TDPrinter, BoxPrinter, OneLinerPrinter

logger = TDLogger(alias="My Custom Logger", printer=OneLinerPrinter()).config()


