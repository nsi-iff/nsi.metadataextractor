Introduction
=====

**nsi.metadataextractor** is a metadata extractor for academic (Portuguese-BR) documents like:

```
Course Conclusion (ABNT format)
Event Article
Periodic Article

Supported extention: .pdf
```

Setup
=====

    pip install nsi.metadataextractor


Example
=====

**Python**

	from nsi.metadataextractor.extractors import tcc, event, periodic
	
	path = "/home/stuff/tccdocument.pdf"
	tccextractor = tcc.TccExtractor(path)
	eventextractor = event.EventExtractor(path)
	periodicextractor = periodic.PeriodicExtractor(path)

	tccextractor.all_metadata()
	eventextractor.all_metadata()
	periodicextractor.all_metadata()


**Bash**
	
	>>> extract_metadata /home/stuff/tccdocument.pdf -t tcc
	>>> extract_metadata /home/stuff/eventdocument.pdf -t event
	>>> extract_metadata /home/stuff/periodicdocument.pdf -t periodic


