#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as readme_file:
    readme = readme_file.read()


setup(
    name="SyntaxMorph",
    version="1.0.1",
    author="Marijua",
    author_email="enderjua@gmail.com",
    description="SyntaxMorph is a Python module that enables code conversion between different programming languages",
    long_description="Description",
    url='https://github.com/Enderjua/SyntaxMorph',
    packages=find_packages(),
    license="GPLv3",
    zip_safe=False,
    keywords='morph, syntax, python, syntaxmorph, ai, machinelearning, change, codexchange',
    install_requires=["openai"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)