=========================
Flake8 __author__ Checker
=========================

|Build Status| |PyPI Version| |Python Versions|

``flake8-author`` is a `Flake8 <https://flake8.readthedocs.org/>`_ extension
that checks Python modules for module-level ``__author__`` attributes.

There is no official standard on ``__author__`` usage. It is used largely by
convention. Guido had this to say `back in 2001`__:

    Anothor source of discomfort is that there's absolutely no standard for
    this kind of meta-data variables.  We've got __version__, and I believe we
    once agreed on that (in 1994 or so :-).  But __author__?  __credits__?
    What next -- __cute_signoff__?

__ https://mail.python.org/pipermail/python-dev/2001-March/013328.html

This extension can therefore be configured to explicitly require or forbid
``__author__`` attributes. By default, ``__author__`` is considered optional.

If the ``__author__`` attribute is allowed, it's value can also be validated
using a configurable pattern.

.. |Build Status| image::  https://img.shields.io/travis/jparise/flake8-author.svg
   :target: https://travis-ci.org/jparise/flake8-author
.. |PyPI Version| image:: https://img.shields.io/pypi/v/flake8-author.svg
   :target: https://pypi.python.org/pypi/flake8-author
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/flake8-author.png
   :target: https://pypi.python.org/pypi/flake8-author


Installation
------------

Install from PyPI using ``pip``:

.. code-block:: sh

    $ pip install flake8-author

The extension will be activated automatically by ``flake8``. You can verify
that it has been loaded by inspecting the ``flake8 --version`` string.

.. code-block:: sh

    $ flake8 --version
    2.5.4 (pep8: 1.7.0, pyflakes: 0.8.1, author: 1.0.1, mccabe: 0.3.1) CPython 2.7.11 on Darwin


Error Codes
-----------

This extension adds three new `warnings`_ (using the ``A40`` prefix):

- ``A400``: a module-level ``__author__`` attribute is required
- ``A401``: ``__author__`` attributes are not allowed
- ``A402``: ``__author__`` attribute value does not match pattern

.. _warnings: http://flake8.readthedocs.io/en/latest/warnings.html

Configuration
-------------

Configuration values are specified in the ``[flake8]`` section of your `config
file`_ or as command line arguments (e.g. ``--author-attribute=required``).

- ``author-attribute``: "optional", "required", "forbidden" (default: optional)
- ``author-pattern``: ``__author__`` validation pattern (default: ``.*``)

.. _config file: http://flake8.readthedocs.io/en/latest/config.html
