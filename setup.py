# -*- coding: utf-8 -*-

# Third
from setuptools import find_packages, setup

__version__ = '1.2.0'
__description__ = 'BTA - Biblioteca de Trabalhos Acadêmicos'
__long_description__ = 'Biblioteca Virtual de Trabalhos Acadêmicos Prof. Me. Silvio José Rosa'

__author__ = 'Pedro Vitorio'
__author_email__ = 'pedro@hotmail.com'

testing_extras = [
    'pytest',
    'pytest-cov',
]

'''setup(
    name='biblioteca-api',
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    packages=find_packages(),
    description=__description__,
    long_description=__long_description__,
    url='http://www.bta.fateccarapicuiba.edu.br/',
    keywords='API, Biblioteca, Trabalhos academicos, Fatec, Carapicuiba',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Students',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    extras_require={
        'testing': testing_extras,
    }
)'''