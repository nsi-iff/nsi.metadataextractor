PYTHON=python
SPECLOUD=specloud

all: install run_unit_test

install:
	${PYTHON} setup.py install

dev:
	${PYTHON} setup.py develop

run_unit_test:
	${SPECLOUD} nsi/metadataextractor/tests/testParser.py
	${SPECLOUD} nsi/metadataextractor/tests/testExtractor.py