import scrapy
from scrapy.loader.processors import TakeFirst, Identity, Join, Compose
import grouch.parsers.prerequisite_parser as pp


class CourseLoader(scrapy.loader.ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = TakeFirst()

    fields_in = Identity()
    fields_out = Identity()

    prerequisites_in = Compose(TakeFirst(), pp.PrerequisiteParser())
    prerequisites_out = TakeFirst()

    corequisites_in = Compose(TakeFirst(), pp.PrerequisiteParser())
    corequisites_out = TakeFirst()

    course_attributes_out = Join()
    restrictions_out = Join()
    grade_basis_out = Join()

