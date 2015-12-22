import unittest
from mock import patch, Mock, MagicMock
from grouch.spiders.oscar_spider import OscarSpider
import scrapy
from grouch.test import PHYS2211
from grouch.loaders import CourseLoader
from grouch.items import Course


class TestSectionParser(unittest.TestCase):

    def setUp(self):
        request = MagicMock()
        request.meta = {'course': CourseLoader(item=Course())}
        self.response = scrapy.http.TextResponse('', body=PHYS2211.body, request=request)
        self.scraper = OscarSpider()

    def test_parse_section(self):
        item = self.scraper.parse_section(self.response)['sections']
        self.assertEqual(len(item), 45)
        for sec in item:
            if sec['crn'] == u'21003':
                self.assertEqual(sec['section_id'], u'B06')
                self.assertEqual(sec['instructors'][0], u'Eric R.  Murray')
                self.assertEqual(sec['meetings'][0]['days'], u'M')
                self.assertEqual(sec['meetings'][0]['location'], u'Clough Undergraduate Commons 123')


