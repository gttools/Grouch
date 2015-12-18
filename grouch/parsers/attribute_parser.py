from grouch.parsers.parser import Parser


class AttributeParser(Parser):
    
    def __init__(self):
        self.methods = [self.splitlines, self.clean, self.split, self.remove_engr]

    @staticmethod
    def splitlines(item):
        return item.splitlines()

    @staticmethod
    def clean(item):
        item = [line.lstrip('<br>') for line in item]
        return [line.strip() for line in item]

    @staticmethod
    def split(item):
        attrs = []
        for line in item:
            attrs.extend(line.split(", "))
        return attrs

    @staticmethod
    def remove_engr(item):
        s = set(item)
        s.discard('')
        if u"Tech Elect CS" in s:
            s.add(u'Tech Elect CS, Engr, &amp;Sciences')
            s.remove(u'Tech Elect CS')
            s.remove(u'Engr')
            s.remove(u'&amp;Sciences')

        return list(s)
