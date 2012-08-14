from setuptools import setup, find_packages
import sys, os

version = '0.0.1'

setup(name='nsi.metadataextractor',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Oswaldo Ferreira',
      author_email='oswluizf@gmail.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        "should_dsl",
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )