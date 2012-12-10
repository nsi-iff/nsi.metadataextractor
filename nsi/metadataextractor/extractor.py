#coding: utf-8
import re
from os import system, remove
from os.path import abspath, dirname, join, basename, splitext
from string import punctuation
from pyPdf import PdfFileReader
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import line_tokenize, word_tokenize
from xml_parser import Parser

ROOT = abspath(dirname(__file__))

class Preparator(object):
    
    def __init__(self, doc_dir):
        self.doc_dir, self.doc_ext = splitext(doc_dir)
        self.doc_name = basename(self.doc_dir)
        self.temp_text_doc = ('%s.txt' %self.doc_name)
        
    def raw_text_convertion(self, page1, page2):
        if self.doc_ext == '.pdf':
            system("pdftotext -enc UTF-8 -f %i -l %i %s.pdf %s.txt"
                %(page1, page2, self.doc_dir, self.doc_dir))
        raw_text = PlaintextCorpusReader(dirname(self.doc_dir), self.temp_text_doc).raw()
        encoded_lowertext = raw_text.decode('utf-8').lower().encode('utf-8')
        self.raw_text = re.sub(r'[0-9]', '', encoded_lowertext)
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

    def pdf_embed_metadata(self):
        embed_metadata = PdfFileReader(file("%s.pdf" %self.doc_dir, "rb"))
        return embed_metadata
        

class TccExtractor(object):

    def __init__(self, doc_dir):
        parse = Parser(join(ROOT, 'templates', 'tcc.xml'))
        self._template_metadata = parse.xml_template_metadata()
        page = self._template_metadata['page']
        pages = self._template_metadata['pages']
        self._preparator = Preparator(doc_dir)
        self._raw_onepage_doc = self._preparator.raw_text_convertion(page, page)
        self._raw_variouspages_doc = self._preparator.raw_text_convertion(pages[0], pages[1])
        self._linetokenized_onepage_raw_doc = open('%s.txt' %self._preparator.doc_dir).readlines()
        self._clean_variouspages_doc = self._raw_variouspages_doc.replace('\n', ' ')
        self._linetokenized_onepage_doc = line_tokenize(self._raw_onepage_doc)
        self._wordtokenized_onepage_doc = [w for w in word_tokenize(self._raw_onepage_doc) if w not in list(punctuation)]
        self.linebreak = "\n"


    def _author_metadata(self):
        self.authors = []
        name_corpus = self._preparator.parse_corpus('names')
        residues = self._template_metadata['author_residue']
        breakers = self._template_metadata['author_breaker']
        for line in self._linetokenized_onepage_doc:
            line_mod = set(word_tokenize(line))
            corpus_common = bool(line_mod.intersection(name_corpus))
            has_residue = bool(line_mod.intersection(residues))
            has_breaker = bool(line_mod.intersection(breakers))
            if corpus_common and not has_residue:
                self.authors.append(line.title())
            elif has_breaker: break
        return self.authors

    def _title_start_point(self):
        self._title_doc = []
        for line in self._linetokenized_onepage_raw_doc:
            self._title_doc.append(line.decode('utf-8').lower().encode('utf-8'))
        authors = self._author_metadata()
        if authors:
            last_author_index = self._title_doc.index(authors[-1].lower() + self.linebreak)
        nextline = last_author_index + 1
        ## Verify line after last author
        if self._title_doc[nextline] == self.linebreak: 
            title_start_point = nextline + 1
        else: title_start_point = last_author_index
        return title_start_point

    def _title_metadata(self):
        self.title = ''
        title_start_point = self._title_start_point()
        breakers = self._template_metadata['title_breaker']
        for title_index in range(title_start_point, len(self._title_doc)):
            line_mod = self._title_doc[title_index].split()
            has_breaker = bool(set(line_mod).intersection(breakers))
            if not has_breaker:
                self.title += self._title_doc[title_index].replace(self.linebreak, ' ')
            else: break
        self.title = self.title.strip().capitalize()
        return self.title

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
        regex = re.compile(r'resumo:* (.*?) (palavr(a|as)(.|\s)chav(e|es).|abstract)')
        self.abstract = regex.search(self._clean_variouspages_doc).group(1).strip().capitalize()
        return self.abstract

    def _grade_metadata(self):
        self.grade = ''
        temp_grade_level = 0
        doc = self._raw_onepage_doc.replace('\n', ' ')
        self.grade_references = {('Graduação', 1):      self._template_metadata['grade_graduation'],
                                 ('Especialização', 2): self._template_metadata['grade_spec'],
                                 ('Mestrado', 3):       self._template_metadata['grade_master_degree'],
                                 ('Doutorado', 4):      self._template_metadata['grade_doctoral'],
                                 ('Pós-Doutorado', 5):  self._template_metadata['grade_postdoctoral']
                                 }
        for grade in self.grade_references.iterkeys():
            grade_type, grade_level = grade
            for grade_name in self.grade_references[grade]:
                if grade_name in doc and grade_level > temp_grade_level:
                    temp_grade_level = grade_level
                    self.grade = grade_type
                    break
        return self.grade

    def all_metadata(self):
        if self._preparator.doc_ext == '.pdf':
            pdf_embed_metadata = self._preparator.pdf_embed_metadata()
            self._pdf_num_pages = pdf_embed_metadata.numPages
        else:
            self._pdf_num_pages = 0

        metadata = {'author_metadata':      self._author_metadata(),
                    'grade_metadata':       self._grade_metadata(),
                    'title_metadata':       self._title_metadata(),
                    'institution_metadata': self._institution_metadata(),
                    'campus_metadata':      self._campus_metadata(),
                    'abstract_metadata':    self._abstract_metadata(),
                    'number_pages':         self._pdf_num_pages
                    }
        try:
            self._preparator.remove_converted_document()
        except OSError:
            print 'Temporary document already removed..'
        return metadata


class EventExtractor(object):        
        
    def __init__(self, doc_dir):
        parse = Parser(join(ROOT, 'templates', 'event.xml'))
        self._template_metadata = parse.xml_template_metadata()
        page = self._template_metadata['page']
        self._preparator = Preparator(doc_dir)
        self._raw_onepage_doc = self._preparator.raw_text_convertion(page, page)
        self._linetokenized_onepage_doc = line_tokenize(self._raw_onepage_doc)
        self._clean_onepage_doc = self._raw_onepage_doc.replace('\n', ' ')
        self._email_regex = re.compile(r'(\w+[.|\w])*@(\w+[.])*\w+')

    def _author_metadata(self):
        self.authors = []
        breaker = self._template_metadata['author_breaker'][0]
        residues = self._template_metadata['author_residue']
        name_corpus = self._preparator.parse_corpus('names') 
        abnt_name = re.compile(r'(\w[.]\s)*(\w+[;])')
        has_only_email = False
        for line in self._linetokenized_onepage_doc:
            has_breaker = re.match(breaker, line)
            if has_breaker: break
            line_mod = set(word_tokenize(line))
            has_corpus_common = bool(line_mod.intersection(name_corpus))
            has_residue = bool(line_mod.intersection(residues))
            if has_corpus_common and not has_residue:
                find_email = self._email_regex.search(line)
                if find_email:
                    email = find_email.group()
                    line = line.replace(email, '').strip()
                self.authors.append(line)
        if not self.authors:
            clean_onepage_doc = self._clean_onepage_doc
            find_author = abnt_name.search(clean_onepage_doc)
            while find_author:
                author = find_author.group()
                self.authors.append(author)
                clean_onepage_doc = clean_onepage_doc.replace(author, '')
                find_author = abnt_name.search(clean_onepage_doc)
        return self.authors

    def _abstract_metadata(self):
        regex = re.compile(r'resumo:* (.*?) palavr(a|as)(.|\s)chav(e|es).')
        self.abstract = regex.search(self._clean_onepage_doc).group(1).strip().capitalize()
        return self.abstract

    def _title_metadata(self):
        self.title = ''
        self.title_catcher = []
        has_author = False
        authors = self._author_metadata()
        breakers = self._template_metadata['title_breaker']
        for line in self._linetokenized_onepage_doc:
            has_breaker = bool(set(word_tokenize(line)).intersection(breakers))
            has_email = self._email_regex.search(line)
            for author in authors:
                has_author = (author in line) or has_author
            if not has_email and not has_author and not has_breaker:
                self.title_catcher.append(line)
            else: 
                self.title = ' '.join(self.title_catcher).capitalize()
                break
        return self.title

    
    def all_metadata(self):
        if self._preparator.doc_ext == '.pdf':
            pdf_embed_metadata = self._preparator.pdf_embed_metadata()
            self._pdf_num_pages = pdf_embed_metadata.numPages
        else:
            self._pdf_num_pages = 0

        metadata = {'author_metadata':      self._author_metadata(),
                    'title_metadata':       self._title_metadata(),
                    'abstract_metadata':    self._abstract_metadata(),
                    'number_pages':         self._pdf_num_pages
                    }
        try:
            self._preparator.remove_converted_document()
        except OSError:
            print 'Temporary document already removed..'
        return metadata
