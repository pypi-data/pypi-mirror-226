# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
  setup_requires='git-versiointi>=1.6rc3',
  name='django-keepdb-tuhoa',
  description='Djangon test-ylläpitokomennon laajennos',
  url='https://github.com/an7oine/django-keepdb-tuhoa.git',
  author='Antti Hautaniemi',
  author_email='antti.hautaniemi@me.com',
  licence='MIT',
  packages=find_packages(),
  include_package_data=True,
  python_requires='>=3.8',
  install_requires=['django>=4.2'],
  entry_points={'django.sovellus': ['keepdb_tuhoa = keepdb_tuhoa']},
  zip_safe=False,
)
