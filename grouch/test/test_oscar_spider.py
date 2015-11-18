import scrapy
import unittest
from mock import patch, MagicMock
import grouch
from grouch import settings
from grouch.spiders.oscar_spider import OscarSpider
from grouch.test import CS1332, catalog

class TestOscarSpider(unittest.TestCase):

    @staticmethod
    def bound_identity(self, *args, **kwargs):
        return args, kwargs

    def setUp(self):
        self.cs1332 = scrapy.http.TextResponse("", body=CS1332.body)
        self.catalog = scrapy.http.TextResponse("", body=catalog.body)
        self.spider = OscarSpider()

    def test_parse_detail(self):
        item = self.spider.parse_detail(self.cs1332)
        self.assertEqual(item['fields'], ["Grade Basis", "Restrictions", "Prerequisites"])
        self.assertEqual(item['fullname'], "CS 1332 - Data Struct & Algorithms")
        self.assertEqual(item['name'], "Data Struct & Algorithms")
        self.assertEqual(item['school'], "CS")
        self.assertEqual(item['number'], "1332")


    # extensive use of mocking below
    def test_parse(self):
        with patch.object(OscarSpider, 'parse_catalog', self.bound_identity):
            result = self.spider.parse(self.cs1332)
            self.assertEqual(result[0][0], self.cs1332)


    def test_parse_catalog(self):
        with patch.object(scrapy, 'FormRequest') as mock:
            results = list(self.spider.parse(self.catalog))
            if settings.SEMESTER_STOP != -1:
                self.assertEqual(len(results), grouch.settings.SEMESTER_STOP)
            call = mock.mock_calls[0]
            self.assertEqual(call[1][0], self.catalog)
            self.assertEqual(call[2], {
                'callback': self.spider.parse_term,
                'formdata': {u'cat_term_in': u'201602'}
                })

