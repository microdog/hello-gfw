__author__ = 'Microdog <dlangu0393@gmail.com>'

import unittest

if __name__ == '__main__':
    loader = unittest.defaultTestLoader.discover('.')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(loader)
