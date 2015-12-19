import scrapy
import unittest
from mock import patch, MagicMock
import grouch
from grouch import settings
from grouch.spiders.oscar_spider import OscarSpider
from grouch.test import CS1332, catalog, term, courses, GRMN4694


class TestOscarSpider(unittest.TestCase):

    @staticmethod
    def bound_identity(self, *args, **kwargs):
        return args, kwargs

    def setUp(self):
        self.cs1332 = scrapy.http.TextResponse("", body=CS1332.body)
        self.german = scrapy.http.TextResponse("", body=GRMN4694.body)
        self.catalog = scrapy.http.TextResponse("", body=catalog.body)
        self.term = scrapy.http.TextResponse("", body=term.body)
        self.courses = scrapy.http.TextResponse("", body=courses.body)

        self.spider = OscarSpider()

    def test_parse_detail(self):
        item = self.spider.parse_detail(self.cs1332)
        self.assertEqual(item['fields'], ["Grade Basis", "Restrictions", "Prerequisites"])
        self.assertEqual(item['fullname'], "CS 1332 - Data Struct & Algorithms")
        self.assertEqual(item['name'], "Data Struct & Algorithms")
        self.assertEqual(item['school'], "CS")
        self.assertEqual(item['number'], "1332")
        self.assertEqual(item['prerequisites'], 
                         {'type': 'or', 'courses' : [u'CS 1322', u'CS 1331']})
        self.assertEqual(item['identifier'], 'CS 1332')

    def test_parse_detail_with_distraction(self):
        """The body of this response contains some wonky stuff that will trick bad regex"""

        item = self.spider.parse_detail(self.german)
        self.assertEqual(item['prerequisites'], {'type': 'and', 'courses': [u'GRMN 2002']})


    # extensive use of mocking below
    def test_parse(self):
        with patch.object(OscarSpider, 'parse_catalog', self.bound_identity):
            result = self.spider.parse(self.cs1332)
            self.assertEqual(result[0][0], self.cs1332)


    def test_parse_catalog(self):
        with patch.object(scrapy, 'FormRequest') as mock:
            results = list(self.spider.parse_catalog(self.catalog))
            if settings.SEMESTER_STOP != -1:
                self.assertEqual(len(results), settings.SEMESTER_STOP)
            call = mock.mock_calls[0]
            self.assertEqual(call[1][0], self.catalog)
            self.assertEqual(call[2], {
                'callback': self.spider.parse_term,
                'formdata': {u'cat_term_in': u'201602'}
                })

    def test_parse_term(self):
        with patch.object(scrapy, 'FormRequest') as mock:
            results = list(self.spider.parse_term(self.term))
            if settings.SUBJECTS:
                self.assertEqual(len(results), len(settings.SUBJECTS))
            subj = settings.SUBJECTS[0] if settings.SUBJECTS else "ACCT"
            # this is a workaround since the subjects parsed can change based on
            # settings in the config file (settings.py), so these tests are
            # invariant to local settings
            call = mock.mock_calls[0]
            self.assertEqual(call[1][0], self.term)
            self.assertEqual(call[2], {
                'callback': self.spider.parse_courses,
                'formdata' : {u'sel_subj': ['dummy', subj]}
                })

    def test_parse_courses(self):
        with patch.object(scrapy, 'Request') as mock:
            results = list(self.spider.parse_courses(self.courses))
            call = mock.mock_calls[0]
            self.assertEqual(len(results), 294)
            self.assertEqual(call[1][0], u'https://oscar.gatech.edu/pls/bprod/bwckctlg.p_disp_course_detail?cat_term_in=201602&subj_code_in=CS&crse_numb_in=1100')
            self.assertEqual(call[1][1], self.spider.parse_detail)
