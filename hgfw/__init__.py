# coding=utf-8

import codecs
import os


def _readline(lines):
    for line in lines:
        yield line.rstrip()


def load_dict(filename, encoding='utf-8'):
    return _readline(codecs.open(filename, 'r', encoding=encoding))


def default_words():
    return load_dict(os.path.join(os.path.dirname(__file__), 'default.dict'), 'utf-8')


class Filter(object):
    def __new__(cls, *args, **kwargs):
        if cls is Filter:
            impl = DFAFilter
        else:
            impl = cls
        instance = super(Filter, cls).__new__(impl)
        instance.__init__(*args, **kwargs)
        return instance

    @classmethod
    def default(cls):
        if cls is Filter:
            cls = DFAFilter

        words = default_words()
        instance = cls(words)
        return instance

    def reload_words(self, words):
        raise NotImplementedError()

    def filter_words(self):
        raise NotImplementedError()

    def contains(self, text):
        """Check if `text` contains any of filtered keywords.

        :param text: text to be tested
        :return: True if filtered keyword found
        """
        raise NotImplementedError()

    def search(self, text):
        """Search filtered keywords in `text`.

        :param text: text to search
        :return: list of (index, keyword) tuple
        """
        raise NotImplementedError()

    def replace(self, text, replace=u'*'):
        """Replace all filtered keywords in `text` with `replace`.

        :param text: text to be tested
        :param replace: the string to replace keyword
        :return: replaced test
        """
        raise NotImplementedError()


class DAWGFilter(Filter):
    def __init__(self, words):
        try:
            import dawg
        except ImportError:
            raise ImportError('Package "DAWG" is required by DAWGFilter.')
        self.dict = dawg.CompletionDAWG
        self.words_dict = self.dict(words)

    def reload_words(self, words):
        new_trie = self.dict(words)
        self.words_dict = new_trie

    def filter_words(self):
        return self.words_dict.keys()

    def contains(self, text):
        words_dict = self.words_dict
        length = len(text)
        for i, c in enumerate(text):
            j = i
            while j < length and words_dict.has_keys_with_prefix(text[i:j + 1]):
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
            while j < length and words_dict.has_keys_with_prefix(text[i:j + 1]):
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
            while j < length and words_dict.has_keys_with_prefix(text[i:j + 1]):
                j += 1
            if text[i:j] in words_dict:
                results.append(new * (j - i))
                i = j
                continue
            results.append(text[i])
            i += 1
        return ''.join(results)


class DFAFilter(Filter):
    ENDING_CHAR = chr(0)

    def __init__(self, words, keep_words=True):
        self.reload_words(words, keep_words)

    def set(self, keywords):
        for word in keywords:
            word += self.ENDING_CHAR
            current_node = self.data
            last_key = None
            last_node = None
            for char in word:
                char = char.lower()
                if current_node is None:
                    current_node = last_node[last_key] = {}
                if not (char in current_node):
                    current_node[char] = None
                    last_node = current_node
                    last_key = char
                current_node = current_node[char]

    def reload_words(self, words, keep_words=True):
        self.data = {}
        if keep_words:
            self.words = list(words)
            self.set(self.words)
        else:
            self.words = None
            self.set(words)

    def _perform(self, text, callback):
        start = 0
        offset = 0
        length = len(text)
        node = self.data

        while start + offset < length:
            char = text[start + offset]
            if char not in node:
                start += 1
                offset = 0
                node = self.data
                continue
            node = node[char]
            offset += 1
            if self.ENDING_CHAR in node:
                if not callback(start, offset, text[start:start + offset]):
                    break
                node = self.data
                start += offset
                offset = 0

    def contains(self, text):
        results = []

        def callback(start, offset, keyword):
            results.append(keyword)
            return False

        self._perform(text, callback)
        return bool(results)

    def search(self, text):
        results = []

        def callback(start, offset, keyword):
            results.append((start, keyword))
            return True

        self._perform(text, callback)
        return results

    def replace(self, text, replace=u'*'):
        segments = []

        def callback(start, offset, keyword):
            segments.append(text[callback.last_index:start])
            segments.append(replace * offset)
            callback.last_index = start + offset
            return True

        callback.last_index = 0

        self._perform(text, callback)
        return ''.join(segments) if segments else text

    def filter_words(self):
        if self.words is not None:
            return self.words
        raise NotImplementedError('Retrieving filter words from DFA\'s internal tree has not been implemented.')
