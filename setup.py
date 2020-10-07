#!/usr/bin/env python3
from setuptools import setup, find_packages

version = "0.0.1-alpha1"

long_description = """
# Placeholder
"""

requirements = []

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
#    packages=find_packages(),
    install_requires=requirements,
    zip_safe=True,
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
    ],
    python_requires='>=3.6',
)
