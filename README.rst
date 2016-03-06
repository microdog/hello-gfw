Hello GFW
=========

A simple text filter for GFW friendly UGC applications.

Usage
-----

Load Dict
~~~~~~~~~

Load dict from iterable:

.. code-block:: python

    >> words_filter = Filter([u'Word1', u'Word2'])

Or load from file using `load_dict` utility, one word per line:

.. code-block:: python

    >> words_iter = load_dict('/path/to/your/dict')
    >> words_filter = Filter(words_iter)

This library also provided a default dict in it, but it is not recommended:

.. code-block:: python

    >> words_filter = Filter.default()

.. note::

    All the words in the default dictionary are collected from internet, and just for testing purpose.

Contains
~~~~~~~~

.. code-block:: python

    >> words_filter.contains(u'There is a keyword.')
    True

Search
~~~~~~

.. code-block:: python

    >> words_filter.search(u'There is a keyword.')
    [(11, u'keyword')]

Replace
~~~~~~~

.. code-block:: python

    >> words_filter.replace(u'There is a keyword.', u'*')
    u'There is a *******.'

Implementations
~~~~~~~~~~~~~~~

Starting from version 0.1, two implementations of Filter are provided: DAWGFilter, DFAFilter(default).
DFAFilter is written in pure Python and has a better performance than DAWGFilter, especially in PyPy.

.. code-block:: python

    >> default_filter = Filter.default()
    >> dawg_filter = DAWGFilter.default()
    >> dfa_filter = DFAFilter.default()

.. note::

    If you want to use DAWGFilter, you need to install `DAWG <https://pypi.python.org/pypi/DAWG>`_ dependency.

Performance
-----------

MacBook Pro (Retina, 13-inch, Early 2015), 3.1 GHz Intel Core i7

DFAFilter with CPython 2.7.10
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

    $ python -m timeit -s "import hgfw; f = hgfw.DFAFilter.default()" "f.contains(u'测试字符串要长长长长一些：成人在线电X，642233，代开发票，作弊仪器，在~家~创~业~。在当前的形 势下，我们要更加积极的举报黄色网站。')"
    100000 loops, best of 3: 36.7 usec per loop

    $ python -m timeit -s "import hgfw; f = hgfw.DFAFilter.default()" "f.search(u'测试字符串要长长长长一些：成人在线电X，642233，代开发票，作弊仪器，在~家~创~业~。在当前的形 势下，我们要更加积极的举报黄色网站。')"
    100000 loops, best of 3: 37.4 usec per loop

    $ python -m timeit -s "import hgfw; f = hgfw.DFAFilter.default()" "f.replace(u'测试字符串要长长长长一些：成人在线电X，642233，代开发票，作弊仪器，在~家~创~业~。在当前的形 势下，我们要更加积极的举报黄色网站。')"
    100000 loops, best of 3: 38.9 usec per loop


DFAFilter with PyPy 4.0.1(2.7.10)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

    $ pypy -m timeit -s "import hgfw; f = hgfw.DFAFilter.default()" "f.contains(u'测试字符串要长长长长一些：成人在线电X，642233，代开发票，作弊仪器，在~家~创~业~。在当前的形 势下，我们要更加积极的举报黄色网站。')"
    1000000 loops, best of 3: 5.95 usec per loop

    $ pypy -m timeit -s "import hgfw; f = hgfw.DFAFilter.default()" "f.search(u'测试字符串要长长长长一些：成人在线电X，642233，代开发票，作弊仪器，在~家~创~业~。在当前的形 势下，我们要更加积极的举报黄色网站。')"
    1000000 loops, best of 3: 5.97 usec per loop

    $ pypy -m timeit -s "import hgfw; f = hgfw.DFAFilter.default()" "f.replace(u'测试字符串要长长长长一些：成人在线电X，642233，代开发票，作弊仪器，在~家~创~业~。在当前的形 势下，我们要更加积极的举报黄色网站。')"
    1000000 loops, best of 3: 6.06 usec per loop

DAWGFilter with CPython 2.7.10
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

    $ python -m timeit -s "import hgfw; f = hgfw.DAWGFilter.default()" "f.contains(u'测试字符串要长长长长一些：成人在线电X，642233，代开发票，作弊仪器，在~家~创~业~。在当前的形 势下，我们要更加积极的举报黄色网站。')"
    10000 loops, best of 3: 64 usec per loop

    $ python -m timeit -s "import hgfw; f = hgfw.DAWGFilter.default()" "f.search(u'测试字符串要长长长长一些：成人在线电X，642233，代开发票，作弊仪器，在~家~创~业~。在当前的形 势下，我们要更加积极的举报黄色网站。')"
    10000 loops, best of 3: 64.8 usec per loop

    $ python -m timeit -s "import hgfw; f = hgfw.DAWGFilter.default()" "f.replace(u'测试字符串要长长长长一些：成人在线电X，642233，代开发票，作弊仪器，在~家~创~业~。在当前的形 势下，我们要更加积极的举报黄色网站。')"
    10000 loops, best of 3: 90.5 usec per loop

TODO
----

* Optimize matching algorithm
* Provide higher-quality dictionaries

License
-------

The MIT License (MIT)

Copyright (c) 2016 Microdog

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Dependency `DAWG <https://github.com/kmike/DAWG/>`_ is licensed under MIT License.
