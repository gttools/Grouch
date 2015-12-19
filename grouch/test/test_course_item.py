import unittest

from grouch import items
from scrapy.loader import ItemLoader


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

