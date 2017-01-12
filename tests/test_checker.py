import ast
import unittest

from flake8.main.application import Application
from flake8_author import Checker


def make_linter(code, path='example.py', argv=None):
    app = Application()
    app.initialize(argv)
    Checker.parse_options(app.options)
    tree = ast.parse(code, path)
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


class TestChecker(unittest.TestCase):

    def test_author_optional(self):
        self.assertIsNone(check('', attribute='optional'))
        self.assertIsNone(check('Jon Parise', attribute='optional'))

    def test_author_required(self):
        self.assertIsNone(check('Jon Parise', attribute='required'))

    def test_author_required_but_missing(self):
        lineno, offset, message, _ = check('', attribute='required')
        self.assertEqual(lineno, 0)
        self.assertEqual(offset, 0)
        self.assertTrue(message.startswith('A400'))

    def test_author_forbidden(self):
        self.assertIsNone(check('', attribute='forbidden'))

    def test_author_forbidden_but_present(self):
        lineno, offset, message, _ = check('Jon Parise', attribute='forbidden')
        self.assertEqual(lineno, 1)
        self.assertEqual(offset, 0)
        self.assertTrue(message.startswith('A401'))

    def test_author_invalid_attribute(self):
        with self.assertRaises(ValueError):
            check('Jon Parise', attribute='invalid')

    def test_author_pattern(self):
        author = 'Jon Parise <jon@example.com>'
        self.assertIsNone(check(author))
        self.assertIsNone(check(author, pattern=r''))
        self.assertIsNone(check(author, pattern=r'.*'))

    def test_author_pattern_not_matched(self):
        author = 'Jon Parise <jon@example.com>'
        lineno, offset, message, _ = check(author, pattern=r'^[\w\s]+$')
        self.assertEqual(lineno, 1)
        self.assertEqual(offset, 0)
        self.assertTrue(message.startswith('A402'))

    def test_author_pattern_invalid_regex(self):
        with self.assertRaises(ValueError):
            check('Jon Parise', pattern=r'[[[')

if __name__ == '__main__':
    unittest.main()
