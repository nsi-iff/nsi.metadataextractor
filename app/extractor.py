#coding: utf-8
from os import path, system, getcwd
from xml_parser import Parser

class Preparator(object):
    
    def __init__(self, doc_type, doc_name):
        self.doc_type = doc_type
        self.doc_name = doc_name
        self.doc_dir = getcwd() +'/app/articles/' +doc_type

    def convert_document(self, page1, page2):
        system("pdftotext -enc UTF-8 -f %i -l %i %s/%s.pdf %s/converted/%s.txt"
            %(page1, page2, self.doc_dir, self.doc_name, self.doc_dir, self.doc_name))
        return self.open_document()
  
    def open_document(self):
        self.document = open('%s/converted/%s.txt' %(self.doc_dir, self.doc_name),'r')
        return self.document.readlines()

    def parse_corpus(self, corpus_type):
        self.corpus_dir = getcwd() + ('/app/corpus/%s.txt' %corpus_type)
        self.corpus = open(self.corpus_dir, 'r').readlines()
        return self.corpus


class TccExtractor(object):

    def __init__(self, doc_name):
        self.preparator = Preparator('obtencaograu', doc_name)
        self.parse = Parser('tcc.xml')
        self.tcc_metadata_hash = self.parse.onepage_metadata.update(self.parse.variouspages_metadata)
        self.page = self.tcc_metadata_hash['page']

    def author_metadata(self):
        self.authors = []
        self.name_corpus = preparator.parse_corpus('names')
        self.doc = self.preparator.convert_document(self.page, self.page)
        #start_position = self.tcc_metadata_hash['author_position']
        self.sucessor = self.tcc_metadata_hash['author_sucessor']
        #while doc[start_position] == antecessor:
        #    start_position += 1
        for line in doc:
            corpus_common = bool(set(line.lower().split()).intersection(self.name_corpus))
            if corpus_common: 
                self.authors.append(line) 
            elif line == sucessor: break
        if not self.authors:
            ### another method to extract authors
            return "authors not found.."
        else: 
            return self.authors

