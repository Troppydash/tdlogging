import re
import threading
import traceback
import time

from tdlogging.tdprinter import TDPrinter
from tdlogging.tdreader import TDReader


class TDLogger:
    __default_config = {
        "exception": False,
        "count": False,
        "exec": True,
        "time": False,
        "return": False,
        "poll": False,
        "poll_period": 5
    }

    current_config = __default_config.copy()
    __information = {}
    alias = ""

    def __init__(self, file_path="tdlogger.txt", config: str = None, alias=""):
        self.alias = alias
        if config is not None:
            self.current_config.update(config)
        else:
            file_content = TDReader.read_from_file(file_path)
            self.__set_config(file_content)

        if self.current_config["poll"] and config is None:
            self.__file_path = file_path
            self.__start_polling()

    @staticmethod
    def __parse_config(string: str) -> dict:
        """
        Parse the string into a config
        :param string: input string
        :return: a config dict
        """
        temp_config = {

        }
        if string:
            # Set configs
            for line in string.split('\n'):
                key_value = re.findall("\w+", line)

                if len(key_value) == 2:
                    if key_value[0] == "poll_period":
                        if re.match("\d", key_value[1]):
                            temp_config[key_value[0]] = int(key_value[1])
                    else:
                        temp_config[key_value[0]] = key_value[1].lower() == "true"
        return temp_config

    def __set_config(self, config_string: str = None) -> dict:
        """
        Set current config from string and return it
        :param config_string: input string - usually from a file read
        :return: current_config
        """
        result_config = TDLogger.__parse_config(config_string)

        cached_config = self.current_config.copy()
        self.current_config.update(result_config)
        if cached_config != self.current_config:
            printer = TDPrinter("Configuration")
            printer.add_dict_message("New Configuration", self.current_config)
            print(printer.get_message())

        return result_config

    def __start_polling(self):
        if not self.current_config['poll']:
            return

        delay = float(self.current_config['poll_period'])
        threading.Timer(delay, self.__start_polling).start()

        ### Update config ###
        text = TDReader.read_from_file(self.__file_path)
        self.__set_config(text)

    @staticmethod
    def __get_arguments(func, argv):
        f_code = func.__code__
        func_parameter = f_code.co_varnames[:f_code.co_argcount + f_code.co_kwonlyargcount]
        arguments = {}
        for i in range(len(func_parameter)):
            if i >= len(argv):
                arguments[func_parameter[i]] = "Undefined"
            else:
                arguments[func_parameter[i]] = argv[i]
        return arguments

    def __start_timer(self, func_name):
        self.__information[func_name]['elapsed_time'] = time.time()

    def __end_timer(self, func_name):
        start_time = self.__information[func_name]['elapsed_time']
        if start_time != -1:
            total_time = time.time() - start_time
            self.__information[func_name]['elapsed_time'] = -1
            return total_time

        return None

    def config(self):
        """
        Gets the logger from a TDLogger Instance that is using config
        :return: logger
        """

        def class_logger(cls):
            def innerLogger(func):
                def wrapper(*argv, **kwargs):
                    # Return Value
                    result = None

                    function_name = func.__name__

                    log_exception = self.current_config['exec'] or self.current_config['exception']
                    log_time = self.current_config['exec'] or self.current_config['time']
                    log_count = self.current_config['exec'] or self.current_config['count']
                    log_return = self.current_config['exec'] or self.current_config['return']
                    log_any = self.current_config['exec'] or self.current_config['count'] \
                              or self.current_config['time'] or self.current_config['return']

                    self.__information[function_name]['execcount'] += 1
                    arguments = self.__get_arguments(func, argv)

                    if log_time:
                        self.__start_timer(function_name)

                    # TODO: Make a new decorator for this
                    if log_exception:
                        try:
                            result = func(*argv, **kwargs)
                        except Exception:
                            printer = TDPrinter("Exception Occurred")
                            printer.add_message("Class: {}".format("TempClass"))
                            printer.add_message("Method: {}".format(function_name))
                            printer.add_message("Count: {}".format(self.__information[function_name]['execcount']))
                            if log_time:
                                total_time = self.__end_timer(function_name)
                                printer.add_message("Exec Time: {:.3f}s".format(total_time))
                            printer.add_dict_message("Arguments", arguments)

                            print(printer.get_message())
                            print(str(traceback.format_exc()))

                            # Re-throw Exception
                            raise
                    else:
                        result = func(*argv, **kwargs)

                    total_time = None
                    if log_time:
                        total_time = self.__end_timer(function_name)

                    if log_any:
                        # Log Arguments
                        printer = TDPrinter("Method Execution")
                        if self.alias:
                            printer.add_message("Alias: {}".format(self.alias))
                        printer.add_message("Class: {}".format(self.__information[function_name]['class_name']))
                        printer.add_message("Method: {}".format(function_name))

                        # Log Count
                        if log_count:
                            printer.add_message("Count: {}".format(self.__information[function_name]['execcount']))

                        # Log Time
                        if log_time:
                            printer.add_message("Exec Time: {:.3f}s".format(total_time))

                        # Log Return
                        if log_return:
                            printer.add_message("Return Value: {}".format(result))
                            printer.add_message("Return Type: {}".format(type(result)))

                        printer.add_dict_message("Arguments", arguments)

                        print(printer.get_message())

                    return result

                return wrapper

            # Apply inside logger to every method
            for attr in cls.__dict__:
                if callable(getattr(cls, attr)):
                    func = getattr(cls, attr)

                    # init methods
                    self.__information[func.__name__] = {
                        "execcount": 0,
                        "elapsed_time": -1.0,
                        "class_name": cls.__name__
                    }

                    setattr(cls, attr, innerLogger(func))
            return cls

        return class_logger
