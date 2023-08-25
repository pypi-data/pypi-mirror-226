#!/usr/bin/env python

import os
from setuptools import setup, find_packages


here = os.path.dirname(os.path.abspath(__file__))
f = open(os.path.join(here, 'README.rst'))
long_description = f.read().strip()
f.close()


setup(
    name='django-rest-auth-e2e',
    version='0.9.6',
    author='rounak kabra',
    author_email='rounak.kabra@e2enetworks.com',
    url='https://github.com/Roniee007/django-rest-auth-e2e',
    description='Create a set of REST API endpoints for Authentication and Registration',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='django rest auth registration rest-framework django-registration api',
    zip_safe=False,
    install_requires=[
        'Django>=1.8.0',
        'djangorestframework>=3.1.3',
        'six>=1.9.0',
    ],
    extras_require={
        'with_social': ['django-allauth>=0.25.0'],
    },
    tests_require=[
        'responses>=0.5.0',
        'django-allauth>=0.25.0',
        'djangorestframework-jwt>=1.9.0',
    ],
    test_suite='runtests.runtests',
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
