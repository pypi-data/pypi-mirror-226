#!/usr/bin/env python
# coding: utf-8
import setuptools
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='WTHMDA',
    version='0.0.4',
    author='qdu-bioinfo',
    author_email='suxq@qdu.edu.cn',
    url='https://github.com/qdu-bioinfo/WTHMDA',
    description="WTHMDA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

)