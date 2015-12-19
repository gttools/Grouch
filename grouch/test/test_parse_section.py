import unittest
import grouch.test.PHYS2211 as PHYS
from grouch.spiders.oscar_spider import OscarSpider as spider
from mock import Mock
from scrapy import Selector

class TestSectionParser(unittest.TestCase):
    def setUp(self):
        self.phys = PHYS.body
        self.mock_course = Mock()
        self.mock_course.meta = {'course': Mock()}
        self.mock_course.css = Mock(return_value=Selector(text=PHYS.body))
        self.spider = spider()

    def test_parse_section(self):
        print self.spider.parse_section(self.mock_course)
        print self.mock_course.call_args_list
        print self.mock_course.meta['course'].add_value.call_args_list
        print self.mock_course.css()
        self.assertEqual(1, 0)

