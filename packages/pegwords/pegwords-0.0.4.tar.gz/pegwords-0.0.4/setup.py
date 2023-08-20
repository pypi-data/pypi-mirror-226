#!/usr/bin/env python

from setuptools import setup
from pathlib import Path
import re


# Modified from http://stackoverflow.com/questions/2058802/
# how-can-i-get-the-version-defined-in-setup-py-setuptools-in-my-package
def version():
    init = Path("pegwords") / "__init__.py"
    with open(init) as fp:
        data = fp.read()
    match = re.search(r"^__version__ = ['\"]([^'\"]+)['\"]", data, re.M)
    if match:
        return match.group(1)

    raise RuntimeError(f"Unable to find version string in {init!r}.")


setup(
    name="pegwords",
    version=version(),
    packages=["pegwords"],
    url="https://github.com/terrycojones/pegwords",
    download_url="https://github.com/terrycojones/pegwords",
    author="Terry C. Jones",
    author_email="terry@jon.es",
    maintainer="Terry C. Jones",
    maintainer_email="terry@jon.es",
    keywords=["pegwords"],
    scripts=[
        "words-to-digits.py",
        "digits-to-words.py",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    description=(
        "Python library and scripts for converting digits to mnemonic "
        "pegwords and back."
    ),
    license="MIT",
)
