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
    fullname = scrapy.Field()  # CS 1332 - Data Struct & Algorithm
    name = scrapy.Field()  # Data Struct & Algorithm
    number = scrapy.Field()  # 1332
    identifier = scrapy.Field()  # CS 1332
    school = scrapy.Field()  # CS
    fields = scrapy.Field()  # subset of "prerequisites, corequisites, grade basis, restrictions, and course_attributes
    prerequisites = scrapy.Field()  # a json structure represeting prerequisite courses
    corequisites = scrapy.Field()  # a json structure representing corequisite courses
    grade_basis = scrapy.Field()  # a string representing grade basis
    restrictions = scrapy.Field()  # a json structure representing course restrictions
    course_attributes = scrapy.Field()  # a list of course attributes
    hours = scrapy.Field()  # a list of hours
    sections = scrapy.Field()  # a json structure representing sections
    semester = scrapy.Field()
    year = scrapy.Field()


class Section(scrapy.Item):
    crn = scrapy.Field()  # the coruse registration number, a 5 digit unique id by semester
    section_id = scrapy.Field()  # section number, like A1
    term = scrapy.Field()  # Spring 2016
    campus = scrapy.Field()  # Georgia Tech-Atlanta * Campus
    meetings = scrapy.Field()  # json structure represeting meeting times
    instructors = scrapy.Field()  # list of instructors

