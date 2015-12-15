import re
import w3lib
from grouch.parsers.parser import Parser


class RestrictionParser(Parser):
    requirement_type = re.compile("(May not be|Must be) enrolled (?:as|in one of) the following (.*?):")

    """
    A parser to convert OSCAR html into json

    From an analysis of an OSCAR data dump, here are some statements about the
    restrictions and their format:
        its divided into lines, these lines can be one of three things:
            <br>
            requirement
            object
        a requirement is a statement in the form
            "(?:May not be|Must be) enrolled (?:as|in one of) the following (.*?):"
        where the following is one of
            "Campuses", "Levels", "Majors", "Classifications", "Programs", "Colleges"

        Following the requirement, there are a series of lines each containing an
        object, these objects can be a variety of things, from "Applied Biology" to
        "Undergraduate Semester", depending on the requirement
    """

    def __init__(self):
        self.methods = [self.remove_tags, self.split, self.clean, self.remove_empty, self.parse]

    @staticmethod
    def remove_tags(item):
        return w3lib.html.remove_tags(item)

    @staticmethod
    def split(item):
        return item.splitlines()

    @staticmethod
    def clean(item):
        item = [line.replace(u'\\u00a0', "") for line in item]
        return [line.strip() for line in item]

    @staticmethod
    def remove_empty(item):
        return [line for line in item if line]

    @staticmethod
    def parse(item):
        d = {'restrictions': []}
        active = None
        for line in item:
            if RestrictionParser.requirement_type.search(line):
                # the line is an outer line
                match = RestrictionParser.requirement_type.search(line)
                d['restrictions'].append(match.group(2))
                d[match.group(2)] = {}
                positive = None
                if match.group(1) == "Must be":
                    positive = True
                else:
                    positive = False
                d[match.group(2)]['positive'] = positive
                d[match.group(2)]['requirements'] = []
                active = match.group(2)
            else:
                d[active]['requirements'].append(line)
        return d

