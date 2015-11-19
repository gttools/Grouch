import scrapy
from scrapy.loader.processors import TakeFirst, Identity, Compose
import w3lib
import re

level = re.compile(r' ?Undergraduate Semester level| ?Graduate Semester level')
grade = re.compile(r' Minimum Grade of [ABCDF]')
splitter = re.compile(r'([A-Z]{2,4} [\dX]{4}|\(|\)|\W+)')

def remove_tags(item):
    return w3lib.html.remove_tags(item)

def strip_irrelevant(item):
    return grade.sub('', level.sub('', item))

def tokenize_and_or(item):
    return re.split(splitter, item)

def remove_whitespace(item):
    return [x.strip() for x in item if x.strip()]

class CourseLoader(scrapy.loader.ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = TakeFirst()

    fields_in = Identity()
    fields_out = Identity()

    prerequisites_in = Compose(TakeFirst(), remove_tags, strip_irrelevant, tokenize_and_or, remove_whitespace)
    prerequisites_out = Identity()

    corequisites_in = Compose(TakeFirst(), remove_tags, strip_irrelevant, tokenize_and_or, remove_whitespace)
    corequisites_out = Identity()