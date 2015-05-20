__author__ = 'Microdog <dlangu0393@gmail.com>'

import dawg
import os
import codecs


DICT = dawg.CompletionDAWG


def _readline(lines):
    for line in lines:
        yield line.rstrip()


def load_dict(filename, encoding='utf-8'):
    return _readline(codecs.open(filename, 'r', encoding=encoding))


def default_words():
    return load_dict(os.path.join(os.path.dirname(__file__), 'default.dict'), 'utf-8')


class Filter(object):

    def __init__(self, words):
        self.words_dict = DICT(words)

    @classmethod
    def default(cls):
        words = default_words()
        instance = Filter(words)
        words.close()
        return instance

    def reload_words(self, words):
        new_trie = DICT(words)
        self.words_dict = new_trie

    def filter_words(self):
        return self.words_dict.keys()

    def contains(self, text):
        words_dict = self.words_dict
        length = len(text)
        for i, c in enumerate(text):
            j = i
            while j < length and words_dict.has_keys_with_prefix(text[i:j+1]):
                j += 1
            if text[i:j] in words_dict:
                return True
        return False

    def search(self, text):
        words_dict = self.words_dict
        length = len(text)
        results = []
        for i, c in enumerate(text):
            j = i
            while j < length and words_dict.has_keys_with_prefix(text[i:j+1]):
                j += 1
            if text[i:j] in words_dict:
                results.append((i, text[i:j]))
        return results

    def replace(self, text, new=u'*'):
        words_dict = self.words_dict
        length = len(text)
        results = []
        i = 0
        while i < length:
            j = i
            while j < length and words_dict.has_keys_with_prefix(text[i:j+1]):
                j += 1
            if text[i:j] in words_dict:
                results.append(new * (j - i))
                i = j
                continue
            results.append(text[i])
            i += 1
        return ''.join(results)
