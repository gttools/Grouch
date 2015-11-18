import scrapy
from scrapy.loader.processors import TakeFirst, Identity


class CourseLoader(scrapy.loader.ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = TakeFirst()

    fields_in = Identity()
    fields_out = Identity()

    field_selector = scrapy.Selector.css