
class Parser(object):
    """
    A generic parser class

    This class has two parts:
         - a methods data item containing a list of functions
         - a __call__ method that calls the functions in the methods field in order on 
           an input value
    """
    def __init__(self):
        self.methods = []

    def __call__(self, item):
        intermediate = item
        for method in self.methods:
            intermediate = method(intermediate)
        return intermediate


