
class Parser(object):
    def __init__(self):
        self.methods = []

    def __call__(self, item):
        intermediate = item
        for method in self.methods:
            intermediate = method(intermediate)
        return intermediate


