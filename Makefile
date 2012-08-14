PYTHON=python

all: install run_unit_test

install:
	${PYTHON} setup.py install

dev:
	${PYTHON} setup.py develop

run_unit_test:
	${PYTHON} nsi/metadataextractor/tests/testParser.py
	${PYTHON} nsi/metadataextractor/tests/testExtractor.py

