from tdlogging.tdlogger import ApplyDecorators, RemoveDecorators

ApplyDecorators(target_dir="cool", import_root="example.logger_instance", var_name="logger", force=True)

fib = []
for i in range(12):
    from example.cool.cooler.sleep import Sleep
    from example.cool.fib import Fib

    fib.append(Fib.get_n(i))
    Sleep.sleep(1)

print("Result: {}".format(fib))
RemoveDecorators(target_dir="cool", import_root="example.logger_instance", var_name="logger", force=True)
