#coding: utf-8
import re
from os.path import abspath, dirname, join, basename, splitext
from nltk.tokenize import line_tokenize, word_tokenize

## Root path
from nsi.metadataextractor.preparator import Preparator
from nsi.metadataextractor.xml_parser import Parser

#Extractor
from nsi.metadataextractor.extractors.event import EventExtractor

ROOT = join(abspath(dirname(__file__)), '..')

class PeriodicExtractor(object):

    def __init__(self, doc_dir):
        convertion_style = "-raw"
        self._eventextractor = EventExtractor(doc_dir)
    	parse = Parser(join(ROOT, 'templates', 'periodic.xml'))
        self._template_metadata = parse.xml_template_metadata()
        page = self._template_metadata['page']
        self._preparator = Preparator(doc_dir)
        self._raw_onepage_doc = self._preparator.raw_text_convertion(page, page, convertion_style)
        self._linetokenized_onepage_doc = line_tokenize(self._raw_onepage_doc)
        self._clean_onepage_doc = self._raw_onepage_doc.replace('\n', ' ')

    ## Event authors metadata extractor extends method to periodic author extractor
    def _author_metadata(self):
        self.authors = self._eventextractor._author_metadata()
        return self.authors

    ## Event abstracts metadata extractor extends method to periodic abstract extractor
    def _abstract_metadata(self):
        self.abstract = self._eventextractor._abstract_metadata()
        return self.abstract

    def all_metadata(self):
        if self._preparator.doc_ext == '.pdf':
            pdf_embed_metadata = self._preparator.pdf_embed_metadata()
            self._pdf_num_pages = pdf_embed_metadata.numPages
        else:
            self._pdf_num_pages = 0

        metadata = {'author_metadata':      self._author_metadata(),
                    'abstract_metadata':    self._abstract_metadata(),
                    'number_pages':         self._pdf_num_pages
                    }
        try:
            self._preparator.remove_converted_document()
        except OSError:
            print 'Temporary document already removed..'
        return metadata