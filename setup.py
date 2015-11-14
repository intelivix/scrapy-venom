# -*- coding: utf-8 -*8-

from setuptools import setup
from setuptools import find_packages


setup(
    name='scrapy-venom',
    packages=find_packages(),
    package_data={
        'scrapy_venom': [],
    },
    version='0.1.1',
    description='Generic classes to deal with data scraping using Scrapy',
    author='Tiago Lira',
    author_email='tiago@intelivix.com',
    url='https://github.com/intelivix/scrapy-venom',
    download_url='https://github.com/intelivix/scrapy-venom/tarball/0.1',
    keywords=['scrapy', 'scraping', 'steps', 'flows'],
    entry_points={
        'console_scripts': [
            'venom = scrapy_venom.command_line:execute_command'
        ]
    },
    install_requires=[
        'Scrapy >= 1.0.2',
    ],
    zip_safe=False,
)
