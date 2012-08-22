#coding: utf-8
from os import system
from os.path import abspath, dirname, join
from xml_parser import Parser

ROOT = abspath(dirname(__file__))

class Preparator(object):
    
    def __init__(self, doc_type, doc_name):
        self.doc_type = doc_type
        self.doc_name = doc_name
        self.doc_dir = join(ROOT, 'articles', self.doc_type)

    def convert_document(self, page1, page2):
        system("pdftotext -enc UTF-8 -f %i -l %i %s/%s.pdf %s/converted/%s.txt"
            %(page1, page2, self.doc_dir, self.doc_name, self.doc_dir, self.doc_name))
        return self.open_document()
  
    def open_document(self):
        self.document = open('%s/converted/%s.txt' %(self.doc_dir, self.doc_name),'r').readlines()
        return self.document

    def parse_corpus(self, corpus_type):
        self.solid_corpus = []
        self.corpus_dir = join(ROOT, 'corpus', '%s.txt' % corpus_type)
        corpus = open(self.corpus_dir, 'r').readlines()
        for item in corpus:
            self.solid_corpus.append(item.strip())
        return self.solid_corpus


class TccExtractor(object):

    def __init__(self, doc_name):
        self.preparator = Preparator('obtencaograu', doc_name)
        self.parse = Parser(join(ROOT, 'templates', 'tcc.xml'))
        self.onepage_metadata = self.parse.onepage_metadata
        self.variouspages_metadata = self.parse.variouspages_metadata
        self.page = self.onepage_metadata['page']
        self.pages = self.parse.variouspages_metadata['pages']
        self.onepage_doc = self.preparator.convert_document(self.page, self.page)
        self.vairouspages_doc = self.preparator.convert_document(self.pages[0], self.pages[1])


    def author_metadata(self):
        self.authors = []
        name_corpus = self.preparator.parse_corpus('names')
        sucessor = self.onepage_metadata['author_sucessor']
        for line_index in range(len(self.onepage_doc) + 1):
            line = self.onepage_doc[line_index].lower().split()
            corpus_common = bool(set(line).intersection(name_corpus))
            if corpus_common:
                self.authors.append(self.onepage_doc[line_index])
            elif self.onepage_doc[line_index] == sucessor[0]:
                break
        if not self.authors:
            ### another method to extract authors
            return 'authors not found..'
        else: 
            return self.authors