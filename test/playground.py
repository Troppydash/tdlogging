from tdlogging.tdlogger import TDLogger, ApplyDecorators, RemoveDecorators


ApplyDecorators(target_dir="cool", import_root="test.logger_instance", var_name="logger", force=True)

for i in range(12):
    from test.cool.cooler.sleep import Sleep
    from test.cool.fib import Fib
    print(Fib.get_n(i))
    Sleep.sleep(1)

RemoveDecorators(target_dir="cool", import_root="test.logger_instance", var_name="logger", force=True)
