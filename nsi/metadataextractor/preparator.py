#coding: utf-8
import re
import sys
from os import system, remove
from os.path import abspath, dirname, join, basename, splitext
from string import punctuation
from pyPdf import PdfFileReader
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import line_tokenize, word_tokenize

ROOT = abspath(dirname(__file__))
CORPUS_PATH = join(ROOT, 'corpus')

class Preparator(object):
    
    def __init__(self, doc_dir):
        self.doc_dir, self.doc_ext = splitext(doc_dir)
        self.doc_name = basename(self.doc_dir)
        self.temp_text_doc = ('%s.txt' %self.doc_name)

    def raw_text_convertion(self, page1, page2, convertion_style):
        if self.doc_ext == '.pdf':
            system("pdftotext -enc UTF-8 -f %i -l %i %s.pdf %s.txt %s"
                %(page1, page2, self.doc_dir, self.doc_dir, convertion_style))
        raw_text = PlaintextCorpusReader(dirname(self.doc_dir), self.temp_text_doc).raw()
        encoded_lowertext = raw_text.decode('utf-8').lower().encode('utf-8')
        self.raw_text = re.sub(r'[0-9]', '', encoded_lowertext)
        return self.raw_text

    def wordtokenized_punctuation_exclusion(self, raw_text):
        wordtokenized_punctuation_excluded = []
        wordtokenized_text = word_tokenize(raw_text)
        for word in wordtokenized_text:
            if word not in list(punctuation):
                wordtokenized_punctuation_excluded.append(word)
        return wordtokenized_punctuation_excluded

    def remove_converted_document(self):
        remove('%s.txt' %self.doc_dir)

    def parse_corpus(self, corpus_type):
        self.corpus_type = '%s.txt' %corpus_type
        self.corpus = line_tokenize(PlaintextCorpusReader(CORPUS_PATH, self.corpus_type).raw().lower())
        if corpus_type == 'institution':
            for line in range(len(self.corpus)):
                self.corpus[line] = self.corpus[line].split(',')
        return self.corpus

    def pdf_embed_metadata(self):
        embed_metadata = PdfFileReader(file("%s.pdf" %self.doc_dir, "rb"))
        return embed_metadata
