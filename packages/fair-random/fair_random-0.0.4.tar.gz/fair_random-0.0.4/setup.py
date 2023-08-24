"""!/usr/bin/env python"""
# coding: utf-8

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fair_random",
    version="0.0.4",
    author="et-repositories",
    author_email="et-repositories@proton.me",
    url="https://github.com/et-repositories/fair-random",
    description="fair random with hash prove",
    long_description=long_description,
    packages=["fair_random"],
    install_requires=[],
)
