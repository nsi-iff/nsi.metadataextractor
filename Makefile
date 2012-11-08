PYTHON=python
SPECLOUD=specloud

all: run_unit_test install

install:
	${PYTHON} setup.py install

dev:
	${PYTHON} setup.py develop

run_unit_test:
	${SPECLOUD} nsi/metadataextractor/tests/testParser.py
	${SPECLOUD} nsi/metadataextractor/tests/testExtractor.py
