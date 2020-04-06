import threading
import traceback
import time

from tdlogging.tdprinter import TDPrinter
from tdlogging.tdreader import TDReader


def create_logger(file_path="tdlogger.txt"):
    """
    Create a TdLogger Instance
    :param file_path: config file path
    :return: TdLogger
    """

    # Default config file
    # Read tdlogger.txt file
    text = TDReader.read_string_from_filepath(file_path)
    config = TDReader.get_config_from_string(text)

    # Return TdLogger Instance
    return TDLogger(config, file_path)


class TDLogger:
    file_path = ""
    # Config
    config = {}

    # Info
    methods = {}

    def __init__(self, config, file_path):
        # A config is required
        if config is None:
            raise Exception("No Logger Config Specified")

        # Set config
        self.config = config
        print(TDPrinter.boxify("Configuration", TDLogger.get_obj_prettified("Configuration", config)))

        # Polling for changes
        self.file_path = file_path
        self.start_polling()

    def start_polling(self):
        self.read_and_modify_config()

    def read_and_modify_config(self):
        if not self.config['poll']:
            return

        threading.Timer(self.config['poll_period'], self.read_and_modify_config).start()
        text = TDReader.read_string_from_filepath(self.file_path, True)
        new_config = TDReader.get_config_from_string(text)
        if new_config != self.config:
            self.config = new_config
            print(TDPrinter.boxify("Configuration updated", TDLogger.get_obj_prettified("New Configuration", new_config)))

    @staticmethod
    def get_argument_prettified(func, argv):
        f_code = func.__code__
        func_parameter = f_code.co_varnames[:f_code.co_argcount + f_code.co_kwonlyargcount]
        argument_pretty = ["Arguments: {"]
        for i in range(len(func_parameter)):
            argument_pretty.append("    '{}': {},".format(func_parameter[i], argv[i]))
        argument_pretty.append("}")
        return argument_pretty

    @staticmethod
    def get_obj_prettified(name, obj: dict) -> list:
        pretty = [name + ": {"]
        for key in obj:
            pretty.append("    '{}': {},".format(key, obj[key]))
        pretty.append('}')
        return pretty

    def start_timer(self, func_name):
        self.methods[func_name]['elapsed_time'] = time.time()

    def end_timer(self, func_name):
        start_time = self.methods[func_name]['elapsed_time']
        if start_time != -1:
            total_time = time.time() - start_time
            self.methods[func_name]['elapsed_time'] = -1
            return total_time

        return None

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

                    function_name = func.__name__

                    # Config
                    log_exception = self.config['exec'] or self.config['exception']
                    log_time = self.config['exec'] or self.config['time']
                    log_count = self.config['exec'] or self.config['count']
                    log_return = self.config['exec'] or self.config['return']
                    log_any = self.config['exec'] or self.config['count'] or self.config['time'] or self.config[
                        'return']

                    # Incre Exec count
                    self.methods[function_name]['execcount'] += 1
                    # Get argument prettified
                    argument_pretty = self.get_argument_prettified(func, argv)
                    # Start Timer
                    if log_time:
                        self.start_timer(function_name)

                    # If catching exceptions
                    if log_exception:
                        # Put function call in try except
                        try:
                            result = func(*argv, **kwargs)
                        except Exception:
                            # Log Everything
                            message = [i for i in argument_pretty]

                            message.append("Times Executed: {}".format(self.methods[function_name]['execcount']))
                            if self.config['exec'] or self.config['time']:
                                total_time = self.end_timer(function_name)
                                message.append(
                                    "Execution Time: {:.3f}s".format(total_time))

                            print(TDPrinter.boxify("Method {} had an exception".format(function_name), message))
                            print(str(traceback.format_exc()))

                            # Re-throw Exeception
                            raise
                    else:
                        result = func(*argv, **kwargs)

                    # End timer
                    total_time = None
                    if log_time:
                        total_time = self.end_timer(function_name)

                    if log_any:
                        # Log Arguments
                        message = [i for i in argument_pretty]

                        # Log Count
                        if log_count:
                            message.append("Times Executed: {}".format(self.methods[function_name]['execcount']))

                        # Log Time
                        if log_time:
                            message.append("Execution Time: {:.3f}s".format(total_time))

                        # Log Return
                        if log_return:
                            message.append("Return Value: {}".format(result))
                            message.append("Return Type: {}".format(type(result)))

                        print(TDPrinter.boxify("Method {} Executed".format(function_name), message))

                    return result

                return wrapper

            # Apply inside logger to every method
            for attr in cls.__dict__:
                if callable(getattr(cls, attr)):
                    func = getattr(cls, attr)

                    # init methods
                    self.methods[func.__name__] = {
                        "execcount": 0,
                        "elapsed_time": -1.0
                    }

                    setattr(cls, attr, innerLogger(func))
            return cls

        return class_logger
