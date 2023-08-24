# coding: utf-8
from setuptools import setup, find_packages

NAME = "pidevguru-piwebapi"
VERSION = "1.0.1"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["six >= 1.10", "requests", "requests-kerberos", "setuptools >= 21.0.0"]

setup(
    name=NAME,
    version=VERSION,
    description="PI Web API client for Python",
    url="https://github.com/pidevguru/PI-Web-API-Client-Python",
    keywords=["PI Web API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    author='Marcos Loeff',
    author_email='pidevguru@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable'
    ],
    long_description="""\
    PI Web API client for Python
    """
)
