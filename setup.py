# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='rdfpandas',
    version='0.1.1',
    description='RDF support for Pandas',
    long_description=readme,
    author='Eugene Morozov',
    author_email='emorozov@gmail.com',
    url='https://github.com/cadmiumkitty/rdfpandas',
    license='MIT',
    packages=find_packages(exclude=('tests', 'docs'))
)

