# coding=utf-8
import unittest

from hgfw import DAWGFilter, DFAFilter


class _FilterTestCase(object):
    keywords = (
        u'中文', u'English', u'Chinese中英文English',
        u'123', u'123abc', u'123 abc',
        u'😄',  # Emotion: laugh
    )

    filter = None

    def filter_factory(self):
        raise NotImplementedError()

    def setUp(self):
        self.filter = self.filter_factory()(self.keywords)

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
        text = u'2222123555中文'

        self.assertEqual([(4, u'123'), (10, u'中文')], self.filter.search(text))

        text2 = u'a1b2c3'

        self.assertEqual([], self.filter.search(text2))

    def test_replace(self):
        text = u'2222123'

        self.assertEqual(u'2222***', self.filter.replace(text))

        text2 = u'a1b2c3'

        self.assertEqual(u'a1b2c3', self.filter.replace(text2))


class DAWGFilterTestCase(_FilterTestCase, unittest.TestCase):
    def filter_factory(self):
        return DAWGFilter


class DFAFilterTestCase(_FilterTestCase, unittest.TestCase):
    def filter_factory(self):
        return DFAFilter
