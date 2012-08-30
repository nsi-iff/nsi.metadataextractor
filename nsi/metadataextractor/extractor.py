#coding: utf-8
from os import system
from re import search
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

    def clean_document_list(self, document_list):
        self.bigstring = ''
        for line in document_list:
            low_line = line.decode('utf-8').lower().encode('utf-8')
            self.bigstring += low_line.replace('\n', ' ').replace(',', '').replace('.', '')
        return self.bigstring.split()

class TccExtractor(object):

    def __init__(self, doc_name):
        self.preparator = Preparator('obtencaograu', doc_name)
        self.parse = Parser(join(ROOT, 'templates', 'tcc.xml'))
        self.onepage_metadata = self.parse.onepage_metadata
        self.variouspages_metadata = self.parse.variouspages_metadata
        self.pages = self.parse.variouspages_metadata['pages']
        self.page = self.onepage_metadata['page']
        self.onepage_doc = self.preparator.convert_document(self.page, self.page)
        self.variouspages_doc = self.preparator.convert_document(self.pages[0], self.pages[1])


    def author_metadata(self):
        self.authors = []
        name_corpus = self.preparator.parse_corpus('names')
        sucessor = self.onepage_metadata['author_sucessor'][0]
        breakers = self.onepage_metadata['author_breaker']
        for line in self.onepage_doc:
            line_mod = set(line.lower().split())
            corpus_common = bool(line_mod.intersection(name_corpus))
            breaker = bool(line_mod.intersection(breakers))
            if corpus_common and not breaker:
                self.authors.append(line)
        return self.authors

    def title_metadata(self):
        i = 0
        self.title = ''
        title_antecessor = self.onepage_metadata['title_antecessor'][0]
        title_sucessor = self.onepage_metadata['title_sucessor'][0]
        first_line = self.onepage_doc.index(title_antecessor) + 1
        doc_range = len(self.onepage_doc)
        for title_type_metadata_index in range(first_line, doc_range):
            if self.onepage_doc[title_type_metadata_index] != title_sucessor:
                self.title += self.onepage_doc[title_type_metadata_index].replace('\n', ' ')
            else: break
        return self.title

    def institution_metadata(self):
        self.institution_names = []
        self.institution_prepositions = []
        self.institution = 'Instituto Federal de Educação Ciência e Tecnologia '
        clean_document_list = self.preparator.clean_document_list(self.onepage_doc)
        institution_list_with_preposition = self.preparator.parse_corpus('institution')
        for item in institution_list_with_preposition:
            item = item.split(',')
            self.institution_prepositions.append(item[0])
            self.institution_names.append(item[1].decode('utf-8').lower().encode('utf-8'))
        for name in self.institution_names:
            name_mod = set(name.split())
            if set(name_mod).intersection(clean_document_list) == name_mod:
                preposition = self.institution_prepositions[self.institution_names.index(name)]
                if preposition:
                    self.institution = self.institution + preposition + ' ' + name.capitalize()
                    break
                else:
                    self.institution += name.capitalize()
                    break
        return self.institution

    def campus_metadata(self):
        self.campus = 'Campus '
        clean_document_list = self.preparator.clean_document_list(self.onepage_doc)
        self.campus_corpus = self.preparator.parse_corpus('campus')
        for campus in self.campus_corpus:
            campus_mod = set(campus.lower().split())
            if set(campus_mod).intersection(clean_document_list) == campus_mod:
                self.campus += campus
                break
        return self.campus

    def abstract_metadata(self):
        self.abstract = ''
        self.abstract_position = 1
        abstract_antecessor = self.variouspages_metadata['abstract_antecessor'][0]
        abstract_sucessor = self.variouspages_metadata['abstract_sucessor'][0]
        if abstract_antecessor not in self.variouspages_doc:
            abstract_antecessor = '\x0c' + abstract_antecessor
        self.abstract_position += self.variouspages_doc.index(abstract_antecessor)
        doc_range = len(self.variouspages_doc)
        while self.variouspages_doc[self.abstract_position] == abstract_sucessor: self.abstract_position += 1
        while self.variouspages_doc[self.abstract_position] != abstract_sucessor:
            self.abstract += self.variouspages_doc[self.abstract_position]
            self.abstract_position += 1
        return self.abstract
