import ast

import pep8
import pytest

from flake8_author import Checker


def make_linter(code, path='example.py', argv=None):
    tree = ast.parse(code, path)
    parser = pep8.get_parser('', '')
    Checker.add_options(parser)
    options, args = parser.parse_args(argv or [])
    Checker.parse_options(options)
    return Checker(tree, path)


def check(author, attribute=None, pattern=None):
    code = '__author__ = "{}"'.format(author) if author else ''

    argv = []
    if attribute:
        argv.append('--author-attribute={}'.format(attribute))
    if pattern:
        argv.append('--author-pattern={}'.format(pattern))

    linter = make_linter(code, argv=argv)
    return next(linter.run(), None)


def test_author_optional():
    assert check('', attribute='optional') is None
    assert check('Jon Parise', attribute='optional') is None


def test_author_required():
    assert check('Jon Parise', attribute='required') is None


def test_author_required_but_missing():
    lineno, offset, message, _ = check('', attribute='required')
    assert lineno == 0
    assert offset == 0
    assert message.startswith('A400')


def test_author_forbidden():
    assert check('', attribute='forbidden') is None


def test_author_forbidden_but_present():
    lineno, offset, message, _ = check('Jon Parise', attribute='forbidden')
    assert lineno == 1
    assert offset == 0
    assert message.startswith('A401')


def test_author_invalid_attribute():
    with pytest.raises(ValueError):
        check('Jon Parise', attribute='invalid')


def test_author_pattern():
    author = 'Jon Parise <jon@example.com>'
    assert check(author) is None
    assert check(author, pattern=r'.*') is None


def test_author_pattern_not_matched():
    author = 'Jon Parise <jon@example.com>'
    lineno, offset, message, _ = check(author, pattern=r'^[\w\s]+$')
    assert lineno == 1
    assert offset == 0
    assert message.startswith('A402')


def test_author_pattern_invalid_regex():
    with pytest.raises(ValueError):
        check('Jon Parise', pattern=r'[[[')
