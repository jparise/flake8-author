Changes
=======

2.1.0 (2023-09-17)
------------------

* Drop support for Python 3.7, and add 3.11.
* Multiple authors can be listed by setting the ``__author__`` attribute to a
  list (or tuple or set) of strings. Each entry will be validated against the
  configured pattern.

2.0.0 (2021-12-30)
------------------

* Drop support for Python 2.7 and 3.6, and add 3.10.
* Drop support for flake8 2.x versions.

1.2.0 (2020-10-12)
------------------

* Drop Python 3.5 support and add versions 3.8 and 3.9.
* Minor documentation improvements.

1.1.4 (2017-07-29)
------------------

* Minor code and packaging cleanup.

1.1.3 (2017-07-28)
------------------

* Drop the ``setup_requires`` dependency on flake8.

1.1.2 (2017-01-12)
------------------

* Only apply the author regular expression pattern check when a pattern has
  actually been configured.

1.1.1 (2016-11-06)
------------------

* Fix configuration file parsing for flake8 3.0+.

1.1.0 (2016-08-15)
------------------

* Support flake8 3.0.0 (required for development)


1.0.2 (2016-06-02)
------------------

* Support flake8 version 2.6.0
* Drop test dependency on pytest (development only)


1.0.1 (2016-05-11)
------------------

* Fixed parser validation for configuration-based options


1.0.0 (2016-04-30)
------------------

* Initial release
