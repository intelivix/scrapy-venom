# -*- coding: utf-8 -*8-

from setuptools import setup
from setuptools import find_packages


setup(
    name='scrapy-venom',
    packages=find_packages(),
    package_data={
        'venom': [],
    },
    version='0.1.1',
    description='Generic classes to deal with data scraping using Scrapy',
    author='Tiago Lira',
    author_email='tiago@intelivix.com',
    url='https://github.com/intelivix/scrapy-venom',
    download_url='https://github.com/intelivix/scrapy-venom/tarball/0.1',
    dependency_links=[
        'https://github.com/arthurmoreno/spider-coverage.git'
        '#egg=spider-coverage'],
    install_requires=[
          'spidercoverage',
      ],
    keywords=['scrapy', 'scraping', 'steps', 'flows'],
    entry_points={
        'console_scripts': [
        ]
    },
    zip_safe=False,
)
