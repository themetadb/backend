#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages  # type: ignore
from tools.utils import get_version

version = get_version()

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = []
    for line in fh.readlines():
        line = line.strip()
        if line:
            requirements.append(line)

setup(
    name='themetadb-backend',
    version=version,
    author='The MetaDB Team',
    author_email='info@themetadb.org',
    description='The MetaDB backend (placeholder)',
    keywords='themetadb, metadb, mdb',
    url='https://github.com/themetadb',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requirements,
    zip_safe=True,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Database',
        'Topic :: Internet',
    ],
    python_requires='>=3.6',
)
