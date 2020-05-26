# -*- coding: utf-8 -*-

# Third
from setuptools import find_packages, setup

__version__ = '0.1.0'
__description__ = 'Biblioteca de Trabalhos Cientificos'
__long_description__ = 'Biblioteca de trabalhos cienteificos para estudantes'

__author__ = 'Pedro Vitorio'
__author_email__ = 'pedro@hotmail.com'

testing_extras = [
    'pytest',
    'pytest-cov',
]

setup(
    name='biblioteca-api',
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    packages=find_packages(),
    license='MIT',
    description=__description__,
    long_description=__long_description__,
    url='https://github.com/lucassimon/flask-api-users.git',
    keywords='API, MongoDB',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers, Students',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    extras_require={
        'testing': testing_extras,
    }
)