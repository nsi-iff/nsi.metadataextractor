Working on ~/nsi.metadataextractor:

Tests:

>>> make run_unit_test



- Course Conclusion Documents (TCC) - Working w/ .pdf files
Example:

>>> from nsi.metadataextractor.extractor import TccExtractor
>>> path = '/Users/osw/Desktop/doctest.pdf'
>>> tccExtract = TccExtractor(path)
>>> tccExtract.all_metadata()