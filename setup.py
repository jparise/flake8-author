#!/usr/bin/env python

import re

from setuptools import setup


def get_version(filename):
    f = open(filename).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", f).group(1)

version = get_version('flake8_author.py')

setup(
    name='flake8-author',
    version=version,
    description='Flake8 __author__ checker',
    long_description=open('README.rst').read(),
    author='Jon Parise',
    author_email='jon@indelible.org',
    keywords='flake8 __author__',
    url='https://github.com/jparise/flake8-author',
    download_url='https://github.com/jparise/flake8-author/tarball/' + version,
    license='MIT',
    py_modules=['flake8_author'],
    entry_points={
        'flake8.extension': ['A40 = flake8_author:Checker'],
    },
    install_requires=['flake8'],
    setup_requires=['flake8', 'pytest-runner'],
    tests_require=['flake8', 'pytest'],
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance'
    ],
)
