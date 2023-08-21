#!/usr/bin/env python
import os
import re

from setuptools import setup

PACKAGE_NAME = "sscred"
INSTALL_REQUIRES = [
    "petlib_fork",
    # "petlib @ git+https://github.com/spring-epfl/petlib.git",
    "attrs",
    # "zksk"
    "zksk_fork"
]
SETUP_REQUIRES = ["pytest-runner"]
TEST_REQUIRES = ["pytest"]


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md")) as f:
    long_description = f.read()


with open(os.path.join(here, PACKAGE_NAME, "__init__.py")) as f:
    matches = re.findall(r"(__.+__) = \"(.*)\"", f.read())
    for var_name, var_value in matches:
        globals()[var_name] = var_value

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    globals()['long_description'] = f.read()


setup(
    name="sscred_fork",
    packages=[PACKAGE_NAME],
    install_requires=INSTALL_REQUIRES,
    setup_requires=SETUP_REQUIRES,
    tests_require=TEST_REQUIRES,
    extras_require={"test": TEST_REQUIRES},
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: BSD License",
    ],
)
