# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class GrouchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Course(scrapy.Item):
    fullname = scrapy.Field()
    name = scrapy.Field()
    number = scrapy.Field()
    school = scrapy.Field()
    fields = scrapy.Field()
    prerequisites = scrapy.Field()
    corequisites = scrapy.Field()
    grade_basis = scrapy.Field()
    restrictions = scrapy.Field()
    course_attributes = scrapy.Field()
