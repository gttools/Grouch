import unittest

from grouch import items

class Test_Course_Item(unittest.TestCase):
    def test_instantiation(self):
        item = items.Course()
        item['name'] = "CS1331"
        self.assertEqual(item['name'], "CS1331")