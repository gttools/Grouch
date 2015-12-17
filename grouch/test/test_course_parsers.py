import unittest
from grouch.parsers.prerequisite_parser import PrerequisiteParser as pp
from grouch.parsers.restriction_parser import RestrictionParser as rp
from grouch.parsers.attribute_parser import AttributeParser as ap
from grouch.parsers.hour_parser import HourParser as hp

class TestPrerequisiteParser(unittest.TestCase):
    maxDiff = None

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

        self.sat_example = ("Undergraduate Semester level MATH 1113 Minimum Grade of D or SAT Mathematics 550 or "
                            "Converted ACT Math 550")

    def test_remove_tags(self):
        string = pp.remove_tags("<b>This is a string</b>")
        self.assertEqual(string, "This is a string")

    def test_strip_irrelevant_handles_level(self):
        strings = []
        strings.append(pp.strip_irrelevant("Undergraduate Semester level CS 1332 or Graduate Semester level CS 2110"))
        strings.append(pp.strip_irrelevant("Undergraduate Semester level CS 2340"))
        strings.append(pp.strip_irrelevant("( Graduate Semester level CS 2340)"))
        self.assertEqual(strings[0], " CS 1332 or CS 2110")
        self.assertEqual(strings[1], " CS 2340")
        self.assertEqual(strings[2], "( CS 2340)")

    def test_strip_irrelevant_handles_grade(self):
        strings = []
        strings.append(pp.strip_irrelevant("CS 1332 Minimum Grade of C"))
        strings.append(pp.strip_irrelevant("CS 2340 Minimum Grade of D"))
        strings.append(pp.strip_irrelevant("( CS 2340 Minimum Grade of F)"))
        self.assertEqual(strings[0], "CS 1332")
        self.assertEqual(strings[1], "CS 2340")
        self.assertEqual(strings[2], "( CS 2340)")

    def test_strip_irrelevant_handles_both(self):
        strings = []
        strings.append(pp.strip_irrelevant("(Undergraduate Semester level CS 3510 Minimum Grade"
                                                " of C or Undergraduate Semester level CS 3511 Minimum Grade of C)"))
        strings.append(pp.strip_irrelevant("and Undergraduate Semester level MATH 3012 Minimum Grade of D and"))
        strings.append(pp.strip_irrelevant(self.long_example))
        # a rediculous real world example
        self.assertEqual(strings[0], "( CS 3510 or CS 3511)")
        self.assertEqual(strings[1], "and MATH 3012 and")
        self.assertEqual(strings[2], ' MATH 3215 or MATH 3770 or MATH 3670 or CEE 3770 or ISYE 3770 or ( ISYE 2027 and ISYE 2028) )')

    def test_tokenize_and_or(self):
        tokenize_list = pp.remove_whitespace(pp.tokenize_and_or(' MATH 3215 or MATH 3770 or MATH 3670 or CEE 3770 or '
                                                                          'ISYE 3770 or ( ISYE 2027 and ISYE 2028) )'))
        self.assertListEqual(tokenize_list, ['MATH 3215', 'or', 'MATH 3770', 'or', 'MATH 3670',
            'or', 'CEE 3770', 'or', 'ISYE 3770', 'or', '(', 'ISYE 2027', 'and', 'ISYE 2028',
            ')', ')'])

    def test_full_series(self):
        longest_example_list = pp.remove_whitespace(pp.tokenize_and_or(
            pp.strip_irrelevant(pp.remove_tags(self.longer_example))))
        self.assertEqual(longest_example_list, ['(', 'CS 3510', 'or', 'CS 3511', ')', 'and',
            'MATH 3012', 'and', '(', 'MATH 3215', 'or', 'MATH 3770', 'or', 'MATH 3670',
            'or', 'CEE 3770', 'or', 'ISYE 3770', 'or', '(', 'ISYE 2027', 'and', 'ISYE 2028',
            ')', ')'])

    def test_parse_tokens(self):
        example_prepped = pp.remove_whitespace(pp.tokenize_and_or(
            pp.strip_irrelevant(pp.remove_tags(self.longer_example))))
        parsed = pp.parse_tokens(example_prepped)
        correct = {'type': 'and', 'courses': [
            {'type' : 'or', 'courses' : [u'CS 3510', u'CS 3511']},
            u'MATH 3012',
            {'type' : 'or', 'courses': [
                u'MATH 3215',
                u'MATH 3770',
                u'MATH 3670',
                u'CEE 3770',
                u'ISYE 3770',
                {'type': 'and', 'courses': [u'ISYE 2027', u'ISYE 2028']}
            ]}
        ]}
        self.assertEqual(parsed, correct)

    def test_sat_act(self):
        example_prepped = pp.remove_whitespace(pp.tokenize_and_or(
            pp.strip_irrelevant(pp.remove_tags(self.sat_example))))
        parsed = pp.parse_tokens(example_prepped)
        correct = {'courses': [u'MATH 1113', u'SAT Mathematics 550', u'ACT Math 550'], 'type': 'or'}
        self.assertEqual(parsed, correct)


class TestRestrictionParser(unittest.TestCase):
    def setUp(self):
        self.string = "\n<br>\nMay not be enrolled in one of the following Levels:\u00a0 \u00a0 \u00a0 \n<br>\n\u00a0 \u00a0 \u00a0 Graduate Semester\n<br>\nMust be enrolled in one of the following Campuses:\u00a0 \u00a0 \u00a0 \n<br>\n\u00a0 \u00a0 \u00a0 Georgia Tech-Atlanta *\n<br>\n<br>\n"

    def test_remove_tags(self):
        cleaned = rp.remove_empty(rp.clean(rp.split(rp.remove_tags(self.string))))
        self.assertEqual(cleaned[0], u'May not be enrolled in one of the following Levels:')
        self.assertEqual(cleaned[1], u'Graduate Semester')
        self.assertEqual(cleaned[2], u'Must be enrolled in one of the following Campuses:')
        self.assertEqual(cleaned[3], u'Georgia Tech-Atlanta *')

    def test_output(self):
        lines = rp.remove_empty(rp.clean(rp.split(rp.remove_tags(self.string))))
        json = rp.parse(lines)
        correct = {'restrictions': [u'Levels', u'Campuses'],
                   u'Levels': {'positive': False, 'requirements': [u'Graduate Semester']},
                   u'Campuses': {'positive': True, 'requirements': [u'Georgia Tech-Atlanta *']}}
        self.assertEqual(json, correct)


class TestAttributeParser(unittest.TestCase):
    def setUp(self):
        self.AS4221 = u'<br>Military Science Course \n<br>\n<br>\n'
        self.AE3120 = u'<br>Tech Elect CS, Engr, &amp;Sciences \n<br>\n<br>\n'
        self.PSYC1101 = u'<br>Ethics Requirement, Social Science Requirement \n<br>\n<br>\n'
        self.CS3210 = u'<br>Computer Systems (CS), Tech Elect CS, Engr, &amp;Sciences \n<br>\n<br>\n'

    def test_basic_attribute_parsing(self):
        parsed = ap()(self.AS4221)
        self.assertSetEqual(set(parsed), set([u'Military Science Course']))

    def test_double_parsed(self):
        parsed = ap()(self.PSYC1101)
        self.assertSetEqual(set(parsed), set([u'Ethics Requirement', u'Social Science Requirement']))

    def test_parse_engr_sciences(self):
        parsed = ap()(self.AE3120)
        self.assertSetEqual(set(parsed), set([u'Tech Elect CS, Engr, &amp;Sciences']))

    def test_parse_engr_sciences_double(self):
        parsed = ap()(self.CS3210)
        self.assertSetEqual(set(parsed), set([u'Tech Elect CS, Engr, &amp;Sciences',
                                              u'Computer Systems (CS)']))

class TestHourParser(unittest.TestCase):
    def setUp(self):
        self.BMED8997 = u'<td class="ntdefault">\nFor graduate students holding a teaching assistantship.\n<br>\n    1.000 TO     9.000 Credit hours\n<br>\n    1.000 TO     9.000 Lecture hours\n<br>\n<br>\n'

    def test_basic_hours(self):
        parsed = hp()(self.BMED8997)
        self.assertEqual(parsed, [u'1.000 TO     9.000 Credit hours', u'1.000 TO     9.000 Lecture hours'])
