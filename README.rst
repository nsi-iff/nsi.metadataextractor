Working on ~/nsi.metadataextractor:

Tests:

>>> make run_unit_test


- Course Conclusion (TCC) and Event Documents - Working w/ .pdf files
Example:

>>> from nsi.metadataextractor.extractor import TccExtractor, EventExtractor
>>> path = '/Users/osw/Desktop/doctest.pdf'
>>> tccExtract = TccExtractor(path)
>>> tccExtract.all_metadata()
>>> eventExtract = EventExtractor(path)
>>> eventExtract.all_metadata()

