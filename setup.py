#!/usr/bin/python3
# -*- coding:utf8 -*-

__author__ = 'Vctcn93'
__version__ = "2019.03.14"

from setuptools import setup, find_packages

packages = find_packages()
lc = open('LICENSE').read()
rm = open('README.MD').read()

setup(
    name="gibbon",
    version="1.0",
    author="Vctcn93",
    author_email="vincentvane@yeah.net",
    description="一个通过高德 API 爬取高德 POI 的服务器",
    license=lc,
    packages=packages,
    long_description=rm,
    install_requires=['numpy', 'pandas', 'pytest'],
    zip_safe=False
)
