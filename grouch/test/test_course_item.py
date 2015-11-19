import unittest

from grouch import items
from scrapy.loader import ItemLoader
from grouch import loaders


class TestCourseItem(unittest.TestCase):
    def test_instantiation(self):
        item = items.Course()
        item['name'] = "CS1331"
        self.assertEqual(item['name'], "CS1331")

    def test_loading(self):
        loader = ItemLoader(item=items.Course())
        loader.add_value('prerequisites', "CS1331")
        loader.add_value('prerequisites', "CS2110")
        item = loader.load_item()
        self.assertEqual(item['prerequisites'], ['CS1331', 'CS2110'])

class TestCourseLoader(unittest.TestCase):
    def setUp(self):
        self.long_example = ("Undergraduate Semester level MATH 3215 Minimum Grade of D or"
            " Undergraduate Semester level MATH 3770 Minimum Grade of D or Undergraduate Semester level MATH 3670"
            " Minimum Grade of D or Undergraduate Semester level CEE 3770 Minimum Grade of D or Undergraduate "
            "Semester level ISYE 3770 Minimum Grade of D or (Undergraduate Semester level ISYE 2027 Minimum Grade "
            "of D and Undergraduate Semester level ISYE 2028 Minimum Grade of D) )")

        self.longer_example = ("(Undergraduate Semester level CS 3510 Minimum ""Grade of C or Undergraduate"
            " Semester level CS 3511 Minimum Grade of C) and Undergraduate Semester level MATH 3012 Minimum Grade "
            "of D and (Undergraduate Semester level MATH 3215 Minimum Grade of D or Undergraduate Semester level MATH "
            "3770 Minimum Grade of D or Undergraduate Semester level MATH 3670 Minimum Grade of D or Undergraduate "
            "Semester level CEE 3770 Minimum Grade of D or Undergraduate Semester level ISYE 3770 Minimum Grade of "
            "D or (Undergraduate Semester level ISYE 2027 Minimum Grade of D and Undergraduate Semester level ISYE "
            "2028 Minimum Grade of D) )")

    def test_remove_tags(self):
        string = loaders.remove_tags("<b>This is a string</b>")
        self.assertEqual(string, "This is a string")

    def test_strip_irrelevant_handles_level(self):
        strings = []
        strings.append(loaders.strip_irrelevant("Undergraduate Semester level CS 1332 or Graduate Semester level CS 2110"))
        strings.append(loaders.strip_irrelevant("Undergraduate Semester level CS 2340"))
        strings.append(loaders.strip_irrelevant("( Graduate Semester level CS 2340)"))
        self.assertEqual(strings[0], " CS 1332 or CS 2110")
        self.assertEqual(strings[1], " CS 2340")
        self.assertEqual(strings[2], "( CS 2340)")

    def test_strip_irrelevant_handles_grade(self):
        strings = []
        strings.append(loaders.strip_irrelevant("CS 1332 Minimum Grade of C"))
        strings.append(loaders.strip_irrelevant("CS 2340 Minimum Grade of D"))
        strings.append(loaders.strip_irrelevant("( CS 2340 Minimum Grade of F)"))
        self.assertEqual(strings[0], "CS 1332")
        self.assertEqual(strings[1], "CS 2340")
        self.assertEqual(strings[2], "( CS 2340)")

    def test_strip_irrelevant_handles_both(self):
        strings = []
        strings.append(loaders.strip_irrelevant("(Undergraduate Semester level CS 3510 Minimum Grade"
                                                " of C or Undergraduate Semester level CS 3511 Minimum Grade of C)"))
        strings.append(loaders.strip_irrelevant("and Undergraduate Semester level MATH 3012 Minimum Grade of D and"))
        strings.append(loaders.strip_irrelevant(self.long_example))
        # a rediculous real world example
        self.assertEqual(strings[0], "( CS 3510 or CS 3511)")
        self.assertEqual(strings[1], "and MATH 3012 and")
        self.assertEqual(strings[2], ' MATH 3215 or MATH 3770 or MATH 3670 or CEE 3770 or ISYE 3770 or ( ISYE 2027 and ISYE 2028) )')

    def test_tokenize_and_or(self):
        tokenize_list = loaders.remove_whitespace(loaders.tokenize_and_or(' MATH 3215 or MATH 3770 or MATH 3670 or CEE 3770 or '
                                                                          'ISYE 3770 or ( ISYE 2027 and ISYE 2028) )'))
        self.assertListEqual(tokenize_list, ['MATH 3215', 'or', 'MATH 3770', 'or', 'MATH 3670',
            'or', 'CEE 3770', 'or', 'ISYE 3770', 'or', '(', 'ISYE 2027', 'and', 'ISYE 2028',
            ')', ')'])

    def test_full_series(self):
        longest_example_list = loaders.remove_whitespace(loaders.tokenize_and_or(
            loaders.strip_irrelevant(loaders.remove_tags(self.longer_example))))
        self.assertEqual(longest_example_list, ['(', 'CS 3510', 'or', 'CS 3511', ')', 'and',
            'MATH 3012', 'and', '(', 'MATH 3215', 'or', 'MATH 3770', 'or', 'MATH 3670',
            'or', 'CEE 3770', 'or', 'ISYE 3770', 'or', '(', 'ISYE 2027', 'and', 'ISYE 2028',
            ')', ')'])
