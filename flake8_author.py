"""Flake8 extension that checks Python modules for an __author__ attribute.

This extension can be configured to explicitly require or forbid __author__
attributes. By default, __author__ is optional.

If the __author__ attribute is allowed, it's value will be validated against a
configurable regular expression pattern (defaults to '.*').
"""

import ast
import re

__author__ = 'Jon Parise'
__version__ = '1.0.1'


class Checker(object):
    """flake8 __author__ checker"""

    name = 'author'
    options = {}
    version = __version__

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename

    @classmethod
    def add_options(cls, parser):
        parser.add_option(
            '--author-attribute',
            default='optional',
            help="__author__ attribute: optional, required, forbidden")
        parser.add_option(
            '--author-pattern',
            default=r'.*',
            help="__author__ attribute validation pattern (regex)")
        parser.config_options.append('author-attribute')
        parser.config_options.append('author-pattern')

    @classmethod
    def parse_options(cls, options):
        choices = ('optional', 'required', 'forbidden')
        if options.author_attribute in choices:
            cls.options['attribute'] = options.author_attribute
        else:
            raise ValueError(
                "author-attribute: '{}' must be one of: {}".format(
                    options.author_attribute, ', '.join(choices)))

        try:
            cls.options['pattern'] = re.compile(options.author_pattern)
        except re.error as e:
            raise ValueError("author-pattern: '{}': {}".format(
                options.author_pattern, e))

    def find_author_node(self, tree):
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue

            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == '__author__':
                    return node

    def run(self):
        node = self.find_author_node(self.tree)

        if node is None and self.options['attribute'] == 'required':
            message = 'A400 module-level __author__ attribute required'
            yield 0, 0, message, type(self)

        elif node and self.options['attribute'] == 'forbidden':
            message = 'A401 __author__ attributes are not allowed'
            yield node.lineno, node.col_offset, message, type(self)

        elif node and not self.options['pattern'].match(node.value.s):
            message = ('A402 __author__ value "{0}" does not match "{1}"'
                       .format(node.value.s, self.options['pattern'].pattern))
            yield node.lineno, node.col_offset, message, type(self)
