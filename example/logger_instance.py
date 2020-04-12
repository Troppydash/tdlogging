from tdlogging.tdlogger import TDLogger
from tdlogging.tdprinter import TDPrinter, BoxPrinter, OneLinerPrinter, CoolPrinter

logger = TDLogger(alias="My Custom Logger", printer=CoolPrinter()).config()


