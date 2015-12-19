from grouch.parsers.parser import Parser


class HourParser(Parser):
    """
    Parses the page for information on credit hours

    Currently very simple implemntation that throws a lot of data away
    """

    def __init__(self):
        self.methods = [self.splitlines, self.strip, self.get_relevant]

    @staticmethod
    def splitlines(item):
        return item.splitlines()

    @staticmethod
    def strip(item):
        return [line.strip() for line in item]

    @staticmethod
    def get_relevant(item):
        hours = []
        for line in item:
            if line[-5:] == 'hours':
                hours.append(line)
        return hours
