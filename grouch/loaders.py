import scrapy
from scrapy.loader.processors import TakeFirst, Identity, Join, Compose
import grouch.parsers.prerequisite_parser as pp
import grouch.parsers.restriction_parser as rp
import grouch.parsers.attribute_parser as ap
import grouch.parsers.hour_parser as hp
import grouch.parsers.basis_parser as bp


class CourseLoader(scrapy.loader.ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = TakeFirst()

    fields_in = Identity()
    fields_out = Identity()

    prerequisites_in = Compose(TakeFirst(), pp.PrerequisiteParser())
    prerequisites_out = TakeFirst()

    corequisites_in = Compose(TakeFirst(), pp.PrerequisiteParser())
    corequisites_out = TakeFirst()

    course_attributes_in = Compose(Join(), ap.AttributeParser())
    course_attributes_out = TakeFirst()

    restrictions_in = Compose(Join(), rp.RestrictionParser())
    restrictions_out = TakeFirst()

    grade_basis_in = Compose(Join(), bp.BasisParser())
    grade_basis_out = Join()

    hours_in = Compose(Join(), hp.HourParser())
    hours_out = TakeFirst()
