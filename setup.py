from setuptools import setup, find_packages
import sys, os

version = '1.0.0'
readme = open('README.rst').read()

setup(name='nsi.metadataextractor',
      version=version,
      description="A template-based metadata extractor.",
      long_description=readme,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='metadata extraction python',
      author='Oswaldo Ferreira',
      author_email='oswluizf@gmail.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        "should_dsl",
        "lxml",
        "specloud",
        "nltk"
      ],
      entry_points = {
            'console_scripts': ['extract_metadata = nsi.metadataextractor.cmdline:main'],
        },
      )
