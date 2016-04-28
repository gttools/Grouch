import re
import w3lib
from grouch.parsers.parser import Parser


class PrerequisiteParser(Parser):
    """
    A parser to convert the OSCAR prerequisite string into a nested json structure
    """
    level = re.compile(r' ?Undergraduate Semester level| ?Graduate Semester level')
    grade = re.compile(r' Minimum Grade of [ABCDFSTU]')
    splitter = re.compile(r'([A-Z]{2,4} [\dX]{4}\w?|\(|\)|\W+)')

    def __init__(self):
        self.methods = [self.remove_tags, self.strip_irrelevant, self.tokenize_and_or,
                        self.remove_whitespace, self.parse_tokens]

    @staticmethod
    def remove_tags(item):
        return w3lib.html.remove_tags(item)

    @staticmethod
    def strip_irrelevant(item):
        return PrerequisiteParser.grade.sub('', PrerequisiteParser.level.sub('', item))

    @staticmethod
    def tokenize_and_or(item):
        return re.split(PrerequisiteParser.splitter, item)

    @staticmethod
    def remove_whitespace(item):
        return [x.strip() for x in item if x.strip()]
    
    @staticmethod
    def _parse_inner(gen, d):
        """
        Converts a string into a nested json structure representing course prerequisites
        via a recursive algorithm
        """
        d['type'] = 'and'
        d['courses'] = []
        for token in gen:
            if token == "(":
                d['courses'].append(PrerequisiteParser._parse_inner(gen, {}))
            elif token == ")":
                return d
            elif token == "and":
                d['type'] = "and"
            elif token == "or":
                d['type'] = "or"
            elif token == "Converted":
                pass
            elif token == "SAT" or token == "ACT":
                d['courses'].append(" ".join((token, next(gen), next(gen))))
            else:
                d['courses'].append(token)
        return d

    @staticmethod
    def parse_tokens(item):
        """
        This deserves a quick explanation. Python generators are like lists that can
        be iterated over exatly once. Once an item is consumed it disappears. In
        this set of functions, the generator is passed down the parse tree. Thus,
        each token is looked at exactly once. This results in an efficient and
        relatively simple parser
        """
        gen = (x for x in item)
        return PrerequisiteParser._parse_inner(gen, {})

