"""Flake8 extension that checks Python modules for an __author__ attribute.

This extension can be configured to explicitly require or forbid __author__
attributes. By default, __author__ is optional.

If the __author__ attribute is allowed, its value will be validated against a
configurable regular expression pattern (defaults to '.*').
"""

import ast
import re
from typing import Literal, Optional, get_args

__author__ = "Jon Parise"
__version__ = "2.2.0"

AttributePolicy = Literal["optional", "required", "forbidden"]


class Checker(object):
    """flake8 __author__ checker"""

    name = "author"
    version = __version__

    # Options
    attribute: AttributePolicy = "optional"
    pattern: Optional[re.Pattern] = None

    def __init__(self, tree, filename):
        self.tree = tree

    @classmethod
    def add_options(cls, parser):
        extra_kwargs = {"parse_from_config": True}

        parser.add_option(
            "--author-attribute",
            default=cls.attribute,
            help="__author__ attribute: {0}".format(
                ", ".join(get_args(AttributePolicy))
            ),
            **extra_kwargs,
        )
        parser.add_option(
            "--author-pattern",
            default=r"",
            help="__author__ attribute validation pattern (regex)",
            **extra_kwargs,
        )

    @classmethod
    def parse_options(cls, options):
        if options.author_attribute in get_args(AttributePolicy):
            cls.attribute = options.author_attribute
        else:
            raise ValueError(
                "author-attribute: '{0}' must be one of: {1}".format(
                    options.author_attribute, ", ".join(get_args(AttributePolicy))
                )
            )

        # Only build a regular expression object when we've been configured
        # with a pattern that doesn't match all strings. This naively just
        # checks for the default empty pattern string as well as `.*`.
        if options.author_pattern and options.author_pattern != ".*":
            try:
                cls.pattern = re.compile(options.author_pattern)
            except re.error as e:
                raise ValueError(
                    "author-pattern: '{0}': {1}".format(options.author_pattern, e)
                )

    def find_author_node(self, tree):
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue

            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__author__":
                    return node

    def _match_author_pattern(self, author, node):
        if self.pattern is not None and not self.pattern.match(author):
            message = 'A402 __author__ value "{0}" does not match "{1}"'.format(
                author, self.pattern.pattern
            )
            yield (node.lineno, node.col_offset, message, type(self))

    def run(self):
        node = self.find_author_node(self.tree)

        if node is None and self.attribute == "required":
            message = "A400 module-level __author__ attribute required"
            yield 0, 0, message, type(self)

        elif node and self.attribute == "forbidden":
            message = "A401 __author__ attributes are not allowed"
            yield node.lineno, node.col_offset, message, type(self)

        elif node and self.pattern is not None:
            if isinstance(node.value, (ast.List, ast.Tuple, ast.Set)):
                for author in ast.literal_eval(node.value):
                    yield from self._match_author_pattern(author, node)
            elif isinstance(node.value, ast.Constant):
                yield from self._match_author_pattern(node.value.value, node)
