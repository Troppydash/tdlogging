import logging
from operator import itemgetter
import json


class TDPrinter:
    _name = "tdlogger"
    _title_padding = 4
    _side_padding = 1
    _title = ""

    messages = ""

    logging_config = {
        "level": logging.DEBUG,
        "format": '%(asctime)s %(levelname)s %(message)s',
        "datefmt": "%d-%b-%y %H:%M:%S",
    }

    def __init__(self, logging_config=None):
        if logging_config is not None:
            self.logging_config.update(logging_config)

    def set_title(self, title: str) -> None:
        self._title = title

    def add_message(self, key, value) -> None:
        self.messages += "|" + str(key) + ": " + str(value)

    def add_dict_message(self, header: str, message: dict) -> None:
        self.messages += "|" + header + ": " + json.dumps(message)

    def log_message(self, level="info"):
        self.messages = "[" + self._title + "]" + self.messages + "|"

        logging.basicConfig(**self.logging_config)
        if level == "info":
            logging.info(self.messages)
        elif level == "error":
            logging.error(self.messages)

        self.messages = ""
        self.set_title("")


class BoxPrinter(TDPrinter):
    __symbols = {
        "top-left": "┌",
        "top-right": "┐",
        "bottom-left": "└",
        "bottom-right": "┘",
        "left-right": "│",
        "top-bottom": "─",
        "padding": " ",
    }
    __width = 50
    messages = []

    def __init__(self, logging_config=None):
        super().__init__(logging_config)

    def set_title(self, title) -> None:
        super().set_title(title)

    def add_message(self, key, value) -> None:
        """
        Add a message to the TDPrinter
        :param key:
        :param value:
        :return:
        """
        self.messages.append("{}: {}".format(key, value))

    def add_dict_message(self, header: str, message: dict) -> None:
        """
        Add a dict message to the TDPrinter
        :param header: the header of message
        :param message: the message dict
        :return:
        """
        self.messages.append(header + ": {")
        for key in message:
            self.messages.append("  '{}': {}".format(key, message[key]))
        self.messages.append("}")

    def log_message(self, level="info"):
        """
        Print the message inside the TDPrinter
        :return:
        """

        return_str = "\n"

        ### Get Box Width excluding side padding ###
        title_total_length = len(self._title) + self._title_padding
        message_list_in_length = [len(i) for i in self.messages]

        message_max_width = 0
        if len(message_list_in_length) != 0:
            message_max_width = max(message_list_in_length)

        box_width = max(title_total_length, message_max_width, len(self._name)) + self._side_padding * 2

        ## Destructing Symbols ##
        top_left, top_right, \
        bottom_left, bottom_right, \
        left_right, top_bottom, \
        padding = itemgetter('top-left', 'top-right',
                             'bottom-left', 'bottom-right',
                             'left-right', 'top-bottom',
                             'padding')(self.__symbols)

        # Add top of the box
        return_str += top_left + str(top_bottom * box_width) + top_right + "\n"

        ### Add Title ###
        title_left_padding = (box_width - title_total_length) / 2
        title_right_padding = int(title_left_padding + 0.5)
        title_left_padding = int(title_left_padding)

        return_str += left_right + str(padding * title_left_padding) \
                      + "--" + self._title + "--" \
                      + str(padding * title_right_padding) + left_right + "\n"

        ### Add messages ###
        for message in self.messages:
            return_str += left_right + padding \
                          + str(message) \
                          + str(padding * (box_width - self._side_padding - len(message))) \
                          + left_right + "\n"

        ### Add TDLOGGER Name
        return_str += left_right + str(padding * (box_width - self._side_padding - len(self._name))) \
                      + self._name \
                      + padding + left_right + "\n"

        ### Add Bottom of box ###
        return_str += bottom_left + str(top_bottom * box_width) + bottom_right + "\n"

        logging.basicConfig(**self.logging_config)
        if level == "info":
            logging.info(return_str)
        elif level == "error":
            logging.error(return_str)

        self.messages = []
        self.set_title("")


class OneLinerPrinter(TDPrinter):
    messages = ""

    def __init__(self, title=""):
        super().__init__(title)

    def set_title(self, title: str) -> None:
        super().set_title(title)

    def add_message(self, key, value) -> None:
        short_key = ""
        for word in key.split():
            short_key += word[0]

        self.messages += "|" + short_key + "->" + str(value)

    def add_dict_message(self, header: str, message: dict) -> None:
        short_header = ""
        for word in str(header).split():
            short_header += word[0]

        short_dict = ""
        for key, item in message.items():
            short_dict += str(key) + ":" + str(item) + ","

        self.messages += "|" + short_header + "->" + "{" + short_dict + "}"

    def log_message(self, level="info"):
        self.messages = "[" + self._title + "]" + self.messages + "|"

        logging.basicConfig(**self.logging_config)
        if level == "info":
            logging.info(self.messages)
        elif level == "error":
            logging.error(self.messages)

        self.messages = ""
        self.set_title("")
