'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-03-19 08:50:01
@LastEditors: feliciaren
@LastEditTime: 2020-05-19 17:22:46
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
    name='automlclient',
    version=find_version(),
    description=
    'A simple automl service http service by aiohttp.',
    packages=find_packages(),
    install_requires=[
       'numpy','requests'
    ])