from setuptools import setup, find_packages
import sys, os

version = '1.2'
readme = open('README.md').read()

setup(name='nsi.metadataextractor',
      version=version,
      description="A template-based metadata extractor.",
      long_description=readme,
      classifiers=[],
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
        "nltk",
        "pyPdf"
      ],
      entry_points = {
            'console_scripts': ['extract_metadata = nsi.metadataextractor.cmdline:main'],
        },
      )
