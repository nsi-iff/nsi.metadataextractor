#coding: utf-8
import re
from os.path import abspath, dirname, join, basename, splitext
from nltk.tokenize import line_tokenize, word_tokenize
from nsi.metadataextractor.preparator import Preparator
from nsi.metadataextractor.xml_parser import Parser

ROOT = join(abspath(dirname(__file__)), '..')

class EventExtractor(object):        
        
    def __init__(self, doc_dir):
        convertion_style = ""
        parse = Parser(join(ROOT, 'templates', 'event.xml'))
        self._template_metadata = parse.xml_template_metadata()
        page = self._template_metadata['page']
        self._preparator = Preparator(doc_dir)
        self._raw_onepage_doc = self._preparator.raw_text_convertion(page, page, convertion_style)
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
                if line != '': self.authors.append(line)
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
        regex = re.compile(r'resumo:* (.*?) (palavr(a|as)(.|\s)chav(e|es).|unitermos|descritores)')
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