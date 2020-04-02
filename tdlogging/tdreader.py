import re

from tdlogging.tdprinter import TDPrinter


class TDReader:
    @staticmethod
    def read_string_from_filepath(file_path, is_polling=False):
        text = ""
        try:
            with open(file_path, 'r') as file:
                text = file.read()
        except:
            if not is_polling:
                print(TDPrinter.boxify("No tdlogger.txt Specified", ["Continuing with default configuration"]))
        return text

    @staticmethod
    def get_config_from_string(string) -> dict:
        config = {
            "exception": False,
            "count": False,
            "exec": True,
            "time": False,
            "return": False,
            "poll": True,
            "poll_period": 5
        }

        if string:
            # Set configs
            for line in string.split('\n'):
                keyvalue = re.findall("\w+", line)

                if len(keyvalue) == 2:
                    if keyvalue[0] == "poll_period":
                        if re.match("\d", keyvalue[1]):
                            config[keyvalue[0]] = int(keyvalue[1])
                    else:
                        config[keyvalue[0]] = keyvalue[1].lower() == "true"

        return config
