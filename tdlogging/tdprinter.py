class TDPrinter:

    @staticmethod
    def boxify(title, messages) -> str:
        """
        Print a pretty box around the title and messages
        :param title: Title of Box
        :param messages: Array of Messages
        :return: Boxified string
        """

        final = ""

        # Get width
        max_length = [len(i) for i in messages]
        max_length.append(len(title) + 4)
        width_without_padding = min(100, max(max(max_length) + 4, 40))

        # Print title
        side_length = (width_without_padding - 10) / 2
        header = "┎"
        if side_length % 2 == 0:
            header += "─" * int(side_length)
        else:
            header += "─" * int(side_length + 0.5)
        header += "TDLogger"
        header += "─" * int(side_length)
        header += "┒"
        final += header + "\n"

        title_length = len(title)
        line = "┃"
        side = ((width_without_padding - 6 - title_length) / 2)

        if side % 2 == 0:
            line += " " * int(side)
        else:
            line += " " * int(side + 0.5)
        line += "--"
        line += title
        line += "--"
        tmp = " " * int(side)
        line += tmp
        line += "┃"

        final += line + "\n"

        for line in messages:
            final += (("┃ " + line).ljust(width_without_padding - 1, " ") + "┃") + "\n"

        # Print bottom
        final += "┖" + "─" * (width_without_padding - 2) + "┚" + "\n"
        return final
