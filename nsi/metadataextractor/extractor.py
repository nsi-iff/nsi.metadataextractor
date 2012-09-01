#coding: utf-8
from os import system, remove
from os.path import abspath, dirname, join
from xml_parser import Parser

ROOT = abspath(dirname(__file__))

class Preparator(object):
    
    def __init__(self, doc_type, doc_name):
        self.doc_type = doc_type
        self.doc_name = doc_name
        self.doc_dir = join(ROOT, 'articles', self.doc_type)

    def convert_document(self, page1, page2):
        system("pdftotext -enc UTF-8 -f %i -l %i %s/%s.pdf %s/%s.txt"
            %(page1, page2, self.doc_dir, self.doc_name, self.doc_dir, self.doc_name))
        return self.open_document()
  
    def open_document(self):
        self.document = open('%s/%s.txt' %(self.doc_dir, self.doc_name),'r').readlines()
        return self.document

    def remove_converted_document(self):
        remove('%s/%s.txt' %(self.doc_dir, self.doc_name))

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
        parse = Parser(join(ROOT, 'templates', 'tcc.xml'))
        self._template_metadata = parse.xml_template_metadata()
        page = self._template_metadata['page']
        pages = self._template_metadata['pages']
        self._preparator = Preparator('obtencaograu', doc_name)
        self._onepage_doc = self._preparator.convert_document(page, page)
        self._variouspages_doc = self._preparator.convert_document(pages[0], pages[1])


    def _author_metadata(self):
        self.authors = []
        name_corpus = self._preparator.parse_corpus('names')
        sucessor = self._template_metadata['author_sucessor'][0]
        residues = self._template_metadata['author_residue']
        for line in self._onepage_doc:
            line_mod = set(line.lower().split())
            corpus_common = bool(line_mod.intersection(name_corpus))
            residue = bool(line_mod.intersection(residues))
            if corpus_common and not residue:
                self.authors.append(line)
        return self.authors

    def _title_metadata(self):
        i = 0
        self.title = ''
        title_antecessor = self._template_metadata['title_antecessor'][0]
        title_sucessor = self._template_metadata['title_sucessor'][0]
        breakers = self._template_metadata['title_breaker']
        first_line = self._onepage_doc.index(title_antecessor) + 1
        doc_range = len(self._onepage_doc)
        for title_type_metadata_index in range(first_line, doc_range):
            line_mod = set(self._onepage_doc[title_type_metadata_index].lower().split())
            breaker = bool(line_mod.intersection(breakers))
            if self._onepage_doc[title_type_metadata_index] != title_sucessor and not breaker:
                self.title += self._onepage_doc[title_type_metadata_index].replace('\n',' ').strip()
            else: break
        return self.title

    def _institution_metadata(self):
        self.institution_names = []
        self.institution_prepositions = []
        self.institution = 'Instituto Federal de Educação Ciência e Tecnologia '
        clean_document_list = self._preparator.clean_document_list(self._onepage_doc)
        institution_list_with_preposition = self._preparator.parse_corpus('institution')
        for item in institution_list_with_preposition:
            item = item.split(',')
            self.institution_prepositions.append(item[0])
            self.institution_names.append(item[1].decode('utf-8').lower().encode('utf-8'))
        for name in self.institution_names:
            name_mod = set(name.split())
            if set(name_mod).intersection(clean_document_list) == name_mod:
                preposition = self.institution_prepositions[self.institution_names.index(name)]
                self.institution = self.institution + preposition + name.capitalize()
                break
        return self.institution

    def _campus_metadata(self):
        self.campus = ''
        clean_document_list = self._preparator.clean_document_list(self._onepage_doc)
        campus_validator = set(self._template_metadata['campus_validator'])
        has_campus = bool(campus_validator.intersection(clean_document_list))
        if has_campus:
            self.campus_corpus = self._preparator.parse_corpus('campus')
            for campus in self.campus_corpus:
                campus_mod = set(campus.lower().split())
                if set(campus_mod).intersection(clean_document_list) == campus_mod:
                    self.campus = campus
                    break
        return self.campus
        
    def _abstract_metadata(self):
        self.abstract = ''
        self.abstract_position = 1
        abstract_antecessor = self._template_metadata['abstract_antecessor'][0]
        abstract_sucessor = self._template_metadata['abstract_sucessor'][0]
        if abstract_antecessor not in self._variouspages_doc:
            abstract_antecessor = '\x0c' + abstract_antecessor
        self.abstract_position += self._variouspages_doc.index(abstract_antecessor)
        doc_range = len(self._variouspages_doc)
        while self._variouspages_doc[self.abstract_position] == abstract_sucessor: self.abstract_position += 1
        while self._variouspages_doc[self.abstract_position] != abstract_sucessor:
            self.abstract += self._variouspages_doc[self.abstract_position]
            self.abstract_position += 1
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
        

