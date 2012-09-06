#coding: utf-8
import sys
from os import listdir
from os.path import abspath, dirname, join, basename

import unittest
from should_dsl import should, should_not
from nsi.metadataextractor.xml_parser import Parser
from nsi.metadataextractor.extractor import Preparator, TccExtractor

ROOT_PATH = abspath(dirname(__file__))
TEMPLATES_PATH = join(ROOT_PATH, '..', 'templates')

class TestPreparation(unittest.TestCase):

	def setUp(self):
		self.parse = Parser('tcc.xml')
		self.doc_dir = '/Users/osw/nsi.metadataextractor/nsi/metadataextractor/articles/obtencaograu/doctest1.pdf'
		self.preparator = Preparator(self.doc_dir)
		self.xml_template_metadata = self.parse.xml_template_metadata()
	
	def test_pdf_document_exists(self):
		document = basename(self.doc_dir)
		documents = listdir(dirname(self.doc_dir))
		document |should| be_into (documents)
	
	def test_pdf_to_txt_convertion(self):
		page = self.xml_template_metadata['page']
		self.preparator.convert_document(page, page)
		documents = listdir(dirname(self.doc_dir))
		self.preparator.temp_text_doc |should| be_into(documents)

	def test_name_corpus_has_a_certain_quantity_of_names(self):
		len(self.preparator.parse_corpus('names')) |should| equal_to(6286)

	def test_temporary_text_files_is_being_removed(self):
		page = self.xml_template_metadata['page']
		documents = listdir(dirname(self.doc_dir))
		self.preparator.convert_document(page, page)
		self.preparator.temp_text_doc |should| be_into(documents)
		self.preparator.remove_converted_document()

		documents = listdir(dirname(self.doc_dir))
		self.preparator.temp_text_doc |should_not| be_into(documents)


	def test_institution_corpus_is_a_list_of_institution_names_with_respective_prepositions(self):
		self.preparator.parse_corpus('institution') |should| equal_to([['', 'fluminense'], ['', 'catarinense'], 
			['', 'baiano'], ['', 'goiano'], ['de ', 'tocantins'], ['do ', 'mato grosso'], ['do ', 'par\xc3\xa1'], 
			['da ', 'para\xc3\xadba'], ['de ', 'sergipe'], ['do ', 'cear\xc3\xa1'], ['de ', 'roraima'], ['de ', 'alagoas'], 
			['de ', 'santa catarina'], ['do ', 'sul de minas'], ['do ', 'sul de minas gerais'], 
			['de ', 's\xc3\xa3o paulo'], ['do ', 'tri\xc3\xa2ngulo mineiro'], ['de ', 'minas gerais'], 
			['do ', 'sert\xc3\xa3o pernambucano'], ['do ', 'mato grosso do sul'], ['da ', 'bahia'], 
			['de ', 'rondonia'], ['do ', 'rio grande do sul'], ['do ', 'rio grande do norte'], ['de ', 'bras\xc3\xadlia'], 
			['do ', 'norte de minas'], ['do ', 'piau\xc3\xad'], ['de ', 'amazonas'], ['do ', 'paran\xc3\xa1'], 
			['de ', 'amap\xc3\xa1'], ['do ', 'acre'], ['de ', 'maranh\xc3\xa3o'], ['do ', 'rio de janeiro'], 
			['de ', 'pernambuco'], ['da ', 'bahia'], ['do ', 'esp\xc3\xadrito santo'], ['do ', 'sudeste de minas gerais'], 
			['de ', 'goi\xc3\xa1s'], ['de ', 'farroupilha'], ['de ', 'goi\xc3\xa1s']])


class TestTccExtractor(unittest.TestCase):

	def setUp(self):
		self.doc_dir = '/Users/osw/nsi.metadataextractor/nsi/metadataextractor/articles/obtencaograu/doctest1.pdf'
		self.preparator = Preparator(self.doc_dir)
		self.extractor = TccExtractor(self.doc_dir)
		self.parse = Parser('tcc.xml')
		self.xml_template_metadata = self.parse.xml_template_metadata()

	def test_has_one_or_more_author_type_metadata_on_a_list(self):
		len(self.extractor._author_metadata()) |should| be_greater_than_or_equal_to(1)
		self.extractor._author_metadata() |should_not| contain('')
		self.preparator.remove_converted_document()

	def test_has_title_type_metadata(self):
		self.extractor._title_metadata() |should_not| equal_to('')
		self.preparator.remove_converted_document()		

 	def test_document_has_a_confirmed_by_corpus_institution_metadata(self):
 		self.extractor._institution_metadata() |should_not| equal_to('Instituto Federal de Educação Ciência e Tecnologia ')
 		self.preparator.remove_converted_document()
 	
 	def test_document_has_a_confirmed_by_corpus_campus_metadata(self):
 		self.extractor._campus_metadata() |should_not| equal_to('')
 		self.preparator.remove_converted_document()

 	def test_document_has_abstract_metadata_type(self):
 		doc = self.extractor._linetokenized_variouspages_raw_doc
 		abstract_antecessor = self.xml_template_metadata['abstract_antecessor'][0]
 		if abstract_antecessor not in doc:
 			abstract_antecessor = '\x0c%s' %abstract_antecessor
		abstract_antecessor |should| be_into(doc)
 		self.extractor._abstract_metadata() |should| end_with('\n')
 		self.preparator.remove_converted_document()


if __name__ == '__main__':
	unittest.main()

	

		
		