import traceback


def class_logger(cls):
    # Inside Logger
    def innerLogger(func):
        def wrapper(*argv, **kwargs):
            try:
                func(*argv, **kwargs)
            except Exception:
                f_code = func.__code__
                func_parameter = f_code.co_varnames[:f_code.co_argcount + f_code.co_kwonlyargcount]

                print("-----An exception happened-----")
                print("Method name: {}".format(func.__name__))
                arg = ""
                for i in range(len(func_parameter)):
                    arg += " '{}': {}".format(func_parameter[i], argv[i])
                print("Arguments: {" + arg, " }")
                print(traceback.format_exc())

                # Re-throw
                raise

        return wrapper

    # Apply inside logger to every method
    for attr in cls.__dict__:
        if callable(getattr(cls, attr)):
            setattr(cls, attr, innerLogger(getattr(cls, attr)))
    return cls
