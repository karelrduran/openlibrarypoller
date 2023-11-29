#!/usr/bin/python3.8
from setuptools import find_packages
from setuptools import setup

setup(
    name='openlibrarypoller',
    version='1.0',
    install_requires=['pandas', 'pymongo[srv]'],
    packages=find_packages(exclude=['notebooks']),
    py_modules=['config'],
    include_package_data=True,
    description='Retrieve books data from Open Library to search by topics'
)
