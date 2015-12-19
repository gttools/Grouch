from grouch.parsers.parser import Parser


class BasisParser(Parser):
    """
    Provides information on grade basis"
    """

    def __init__(self):
        self.methods = [self.splitlines, self.take_first]

    @staticmethod
    def splitlines(item):
        return item.splitlines()

    @staticmethod
    def take_first(item):
        return item[0].strip()
