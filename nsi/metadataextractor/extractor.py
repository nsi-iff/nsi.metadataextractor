#coding: utf-8
from os import system, remove
from os.path import abspath, dirname, join, basename, splitext
from string import punctuation
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import line_tokenize, word_tokenize
from xml_parser import Parser

ROOT = abspath(dirname(__file__))

class Preparator(object):
    
    def __init__(self, doc_dir):
        self.doc_dir, self.doc_ext = splitext(doc_dir)
        self.doc_name = basename(self.doc_dir)
        self.temp_text_doc = ('%s.txt' %self.doc_name)
        

    def convert_document(self, page1, page2):
        system("pdftotext -enc UTF-8 -f %i -l %i %s.pdf %s.txt"
            %(page1, page2, self.doc_dir, self.doc_dir))
        self.raw_text = PlaintextCorpusReader(dirname(self.doc_dir), self.temp_text_doc).raw().lower()
        return self.raw_text

    def remove_converted_document(self):
        remove('%s.txt' %self.doc_dir)

    def parse_corpus(self, corpus_type):
        self.corpus_type = '%s.txt' %corpus_type
        self.corpus_dir = join(ROOT, 'corpus')
        self.corpus = line_tokenize(PlaintextCorpusReader(self.corpus_dir, self.corpus_type).raw().lower())
        if corpus_type == 'institution':
            for line in range(len(self.corpus)):
                self.corpus[line] = self.corpus[line].split(',')
        return self.corpus


class TccExtractor(object):

    def __init__(self, doc_dir):
        parse = Parser(join(ROOT, 'templates', 'tcc.xml'))
        self._template_metadata = parse.xml_template_metadata()
        page = self._template_metadata['page']
        pages = self._template_metadata['pages']
        self._preparator = Preparator(doc_dir)
        self._raw_onepage_doc = self._preparator.convert_document(page, page)
        self._linetokenized_onepage_raw_doc = open('%s.txt' %self._preparator.doc_dir).readlines()
        self._raw_variouspages_doc = self._preparator.convert_document(pages[0], pages[1])
        self._linetokenized_variouspages_raw_doc = open('%s.txt' %self._preparator.doc_dir).readlines()
        self._linetokenized_onepage_doc = line_tokenize(self._raw_onepage_doc)
        self._wordtokenized_onepage_doc = [w for w in word_tokenize(self._raw_onepage_doc) if w not in list(punctuation)]


    def _author_metadata(self):
        self.authors = []        
        name_corpus = self._preparator.parse_corpus('names')
        residues = self._template_metadata['author_residue']
        for line in self._linetokenized_onepage_doc:
            line_mod = set(word_tokenize(line))
            corpus_common = bool(line_mod.intersection(name_corpus))
            residue = bool(line_mod.intersection(residues))
            if corpus_common and not residue:
                self.authors.append(line.title())
        return self.authors

    def _title_metadata(self):
        self.title = ''
        title_antecessor = self._template_metadata['title_antecessor'][0]
        title_sucessor = self._template_metadata['title_sucessor'][0]
        breakers = self._template_metadata['title_breaker']
        first_line = self._linetokenized_onepage_raw_doc.index(title_antecessor) + 1
        doc_range = len(self._linetokenized_onepage_raw_doc)
        for title_type_metadata_index in range(first_line, doc_range):
            line_mod = set(word_tokenize(self._linetokenized_onepage_raw_doc[title_type_metadata_index]))
            breaker = bool(line_mod.intersection(breakers))
            if self._linetokenized_onepage_raw_doc[title_type_metadata_index] != title_sucessor and not breaker:
                self.title += self._linetokenized_onepage_raw_doc[title_type_metadata_index].replace('\n',' ')
            else: break
        return self.title.strip()

    def _institution_metadata(self):
        self.institution = 'Instituto Federal de Educação Ciência e Tecnologia '
        institution_validator = set(self._template_metadata['institution_validator'])
        has_institution = bool(institution_validator.intersection(self._wordtokenized_onepage_doc))
        if has_institution:
            institution_corpus = self._preparator.parse_corpus('institution')
            for preposition, institution in institution_corpus:
                name_mod = set(institution.split())
                if name_mod.intersection(self._wordtokenized_onepage_doc) == name_mod:
                    self.institution = self.institution + preposition + institution.title()
                    break
        return self.institution

    def _campus_metadata(self):
        self.campus = ''
        campus_validator = set(self._template_metadata['campus_validator'])
        has_campus = bool(campus_validator.intersection(self._wordtokenized_onepage_doc))
        if has_campus:
            self.campus_corpus = self._preparator.parse_corpus('campus')
            for campus in self.campus_corpus:
                campus_mod = set(campus.split())
                if campus_mod.intersection(self._wordtokenized_onepage_doc) == campus_mod:
                    self.campus = campus.title()
                    break
        return self.campus
        
    def _abstract_metadata(self):
        self.abstract = ''
        abstract_antecessor = self._template_metadata['abstract_antecessor'][0]
        abstract_sucessor = self._template_metadata['abstract_sucessor'][0]
        if abstract_antecessor not in self._linetokenized_variouspages_raw_doc:
            abstract_antecessor = '\x0c%s' %abstract_antecessor
        abstract_position = self._linetokenized_variouspages_raw_doc.index(abstract_antecessor) + 1
        doc_range = len(self._linetokenized_variouspages_raw_doc)
        while self._linetokenized_variouspages_raw_doc[abstract_position] == abstract_sucessor:
            abstract_position += 1
        while self._linetokenized_variouspages_raw_doc[abstract_position] != abstract_sucessor:
            self.abstract += self._linetokenized_variouspages_raw_doc[abstract_position]
            abstract_position += 1
        return self.abstract
        


    def all_metadata(self):
        metadata = {'author_metadata':      self._author_metadata(),
                    'title_metadata':       self._title_metadata(),
                    'institution_metadata': self._institution_metadata(),
                    'campus_metadata':      self._campus_metadata(),
                    'abstract_metadata':    self._abstract_metadata(),
                    }
        self._preparator.remove_converted_document()
        return metadata
        

