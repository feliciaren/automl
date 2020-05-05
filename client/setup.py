'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-03-19 08:50:01
@LastEditors: feliciaren
@LastEditTime: 2020-03-19 08:58:55
'''
'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-03-18 23:15:11
@LastEditors: feliciaren
@LastEditTime: 2020-03-19 07:45:24
'''
from setuptools import setup, find_packages
import os
import re


def find_version():
    fn = os.path.join(os.path.dirname(__file__), '', 'version.py')
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              open(fn).read(), re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='automl_serving',
    version=find_version(),
    description=
    'A simple automl service http client.',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    entry_points={
        'console_scripts': ['ner-client=cmd:entry_point'],
    })