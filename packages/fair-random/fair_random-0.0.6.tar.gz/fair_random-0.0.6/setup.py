"""!/usr/bin/env python"""
# coding: utf-8

from pathlib import Path
from setuptools import setup


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="fair_random",
    version="0.0.6",
    author="et-repositories",
    author_email="et-repositories@proton.me",
    url="https://github.com/et-repositories/fair-random",
    description="fair random with hash prove",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["fair_random"],
    install_requires=[],
)
