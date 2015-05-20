# coding=utf-8
__author__ = 'Microdog <dlangu0393@gmail.com>'

import unittest

from hgfw import Filter


class FilterTestCase(unittest.TestCase):

    keywords = (
        u'中文', u'English', u'Chinese中英文English',
        u'123', u'123abc', u'123 abc',
        u'😄',  # Emotion: laugh
    )

    filter = None

    def setUp(self):
        self.filter = Filter(self.keywords)

    def test_filter_words(self):
        self.assertEqual(set(self.keywords), set(self.filter.filter_words()))

    def test_reload_words(self):
        self.assertEqual(set(self.keywords), set(self.filter.filter_words()))

        new_words = (u'test', u'321')

        self.filter.reload_words(new_words)

        self.assertEqual(set(new_words), set(self.filter.filter_words()))

        self.filter.reload_words(self.keywords)

    def test_contains(self):
        text = u'1a2b3c abc 123'

        self.assertTrue(self.filter.contains(text))

        text2 = u'a1b2c3 abc'

        self.assertFalse(self.filter.contains(text2))

    def test_search(self):
        text = u'123 abc'

        self.assertEqual([(0, u'123 abc')], self.filter.search(text))

        text2 = u'a1b2c3'

        self.assertEqual([], self.filter.search(text2))

    def text_replace(self):
        text = u'123 abc'

        self.assertEqual(u'*** ***', self.filter.replace(text))

        text2 = u'a1b2c3'

        self.assertEqual(u'a1b2c3', self.filter.replace(text2))
