import scrapy
from scrapy.loader.processors import TakeFirst, Identity, Compose, Join
import w3lib
import re

level = re.compile(r' ?Undergraduate Semester level| ?Graduate Semester level')
grade = re.compile(r' Minimum Grade of [ABCDFSTU]')
splitter = re.compile(r'([A-Z]{2,4} [\dX]{4}|\(|\)|\W+)')

def remove_tags(item):
    return w3lib.html.remove_tags(item)

def strip_irrelevant(item):
    return grade.sub('', level.sub('', item))

def tokenize_and_or(item):
    return re.split(splitter, item)

def remove_whitespace(item):
    return [x.strip() for x in item if x.strip()]

def _parse_inner(gen, d):
    """
    Converts a string into a nested json structure representing course prerequisites
    via a recursive algorithm
    """
    d['type'] = 'and'
    d['courses'] = []
    for token in gen:
        if token == "(":
            d['courses'].append(_parse_inner(gen, {}))
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


def parse_tokens(item):
    """
    This deserves a quick explanation. Python generators are like lists that can
    be iterated over exatly once. Once an item is consumed it disappears. In
    this set of functions, the generator is passed down the parse tree. Thus,
    each token is looked at exactly once. This results in an efficient and
    relatively simple parser
    """
    gen = (x for x in item)
    return _parse_inner(gen, {})


class CourseLoader(scrapy.loader.ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = TakeFirst()

    fields_in = Identity()
    fields_out = Identity()

    prerequisites_in = Compose(TakeFirst(), remove_tags, strip_irrelevant, tokenize_and_or, remove_whitespace, parse_tokens)
    prerequisites_out = TakeFirst()

    corequisites_in = Compose(TakeFirst(), remove_tags, strip_irrelevant, tokenize_and_or, remove_whitespace, parse_tokens)
    corequisites_out = TakeFirst()

    course_attributes_out = Join()
    restrictions_out = Join()
    grade_basis_out = Join()

