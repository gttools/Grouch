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

    corequisites_in = Compose(TakeFirst(), pp.PrerequisiteParser())

    course_attributes_in = Compose(Join(), ap.AttributeParser())

    restrictions_in = Compose(Join(), rp.RestrictionParser())
    restrictions_out = TakeFirst()

    grade_basis_in = Compose(Join(), bp.BasisParser())
    grade_basis_out = Join()

    hours_in = Compose(Join(), hp.HourParser())

    sections_in = Identity()
    sections_out = Identity()


class SectionLoader(scrapy.loader.ItemLoader):
    default_input_processor = TakeFirst()
    default_output_processor = TakeFirst()

    meetings_in = Identity()
    meetings_out = Identity()

    instructors_in = Identity()
    instructors_out = Identity()
