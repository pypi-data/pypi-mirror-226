#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     :
# @Author   : wgh

from setuptools import setup, find_packages
import os

VERSION = '0.0.1'
DESCRIPTION = 'Easily test'

setup(
    name="wgh_yt_test",
    version=VERSION,
    author="guohuai wu",
    author_email="wu466687121@qq.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md', encoding="UTF8").read(),
    packages=find_packages(),
    install_requires=['moviepy'],
    keywords=['python', 'moviepy', 'cut video'],
    data_files=[('testjson', ['test.json'])],
    entry_points={
    'console_scripts': [
        'cut_video = cut_video.main:main'
    ]
    },
    license="MIT",
    url="https://gitee.com/Sea-Depth/wgh_yt_test.git",
    scripts=['main.py'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ]
)
