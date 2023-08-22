# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text(encoding="UTF-8")

setup(
    name='billionprompt',
    version='0.0.2',
    author='ShanHai AI',
    author_email='xiexiaofeng@youxiqun.com',
    description='BillionPrompt Python SDK',
    url='',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
    ],
    long_description=README,
    long_description_content_type='text/markdown',
)