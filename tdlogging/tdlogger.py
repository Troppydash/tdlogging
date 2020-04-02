import time
import traceback
import re

from tdlogging.tdprinter import TDPrinter


def create_logger(path="tdlogger.txt"):
    """
    Create a TdLogger Instance
    :param path: config file path
    :return: TdLogger
    """

    # Default config file
    config = {
        "exception": False,
        "count": False,
        "exec": True,
        "time": False,
        "return": False
    }

    # Read tdlogger.txt file
    f = open(path, 'r')
    txt = f.read()

    if txt:
        # Set configs
        for line in txt.split('\n'):
            keyvalue = re.findall("\w\w*\w", line)

            if len(keyvalue) == 2:
                config[keyvalue[0]] = keyvalue[1].lower() == "true"
    # Return TdLogger Instance
    return TDLogger(config)


class TDLogger:
    config = {}

    # Cached Info
    info = {
        "execcount": 0,
        "elapsed_time": 0.0
    }

    def __init__(self, config):
        # A config is required
        if config is None:
            raise Exception("A Logger Config is Required")
        # Set config
        self.config = config

    def get_logger(self):
        """
        Gets the logger from a TDLogger Instance
        :return: logger
        """
        def class_logger(cls):
            def innerLogger(func):
                def wrapper(*argv, **kwargs):
                    # Return Value
                    result = None

                    # Incre Exec count
                    self.info['execcount'] += 1

                    # Get argument prettified
                    f_code = func.__code__
                    func_parameter = f_code.co_varnames[:f_code.co_argcount + f_code.co_kwonlyargcount]
                    argument_pretty = ["Arguments: {"]
                    for i in range(len(func_parameter)):
                        argument_pretty.append("    '{}': {},".format(func_parameter[i], argv[i]))
                    argument_pretty.append("}")

                    # Start Timer
                    start_time = None
                    if self.config['time'] or self.config['exec']:
                        start_time = time.time()

                    # If catching exceptions
                    if self.config['exception']:
                        # Put function call in try except
                        try:
                            result = func(*argv, **kwargs)
                        except Exception:
                            # Log Everything except time
                            message = [i for i in argument_pretty]

                            message.append("Times Executed: {}".format(self.info['execcount']))

                            print(TDPrinter.boxify("Method {} had an exception".format(func.__name__), message))
                            print(str(traceback.format_exc()))

                            # Re-throw Exeception
                            raise
                    else:
                        result = func(*argv, **kwargs)

                    # End timer
                    if start_time is not None:
                        self.info['elapsed_time'] = time.time() - start_time

                    if self.config['exec'] or self.config['count'] or self.config['time'] or self.config['return']:
                        # Log Arguments
                        message = [i for i in argument_pretty]

                        # Log Count
                        if self.config['exec'] or self.config['count']:
                            message.append("Times Executed: {}".format(self.info['execcount']))

                        # Log Time
                        if self.config['exec'] or self.config['time']:
                            message.append("Execution Time: {:.3f}s".format(self.info['elapsed_time']))

                        # Log Return
                        if self.config['exec'] or self.config['return']:
                            message.append("Return Value: {}".format(result))
                            message.append("Return Type: {}".format(type(result)))

                        print(TDPrinter.boxify("Method {} Executed".format(func.__name__), message))
                    return result

                return wrapper

            # Apply inside logger to every method
            for attr in cls.__dict__:
                if callable(getattr(cls, attr)):
                    setattr(cls, attr, innerLogger(getattr(cls, attr)))
            return cls

        return class_logger
