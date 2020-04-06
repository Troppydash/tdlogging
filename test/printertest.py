from tdlogging.tdprinter import TDPrinter

printer = TDPrinter("Yessadasdasdas")
printer.add_message("Hello: World")
printer.add_message("Hello: Yessadasdasdas")
print(printer.get_message())
print(printer.get_message())