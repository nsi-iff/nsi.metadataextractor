PYTHON=python
SPECLOUD=specloud

all: install run_unit_test

run_unit_test:
	$(SPECLOUD) app/tests/testParser.py  && $(SPECLOUD) app/tests/testExtractor.py

