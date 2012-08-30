#coding: utf-8
import sys
from os import listdir
from os.path import abspath, dirname, join

import unittest
from should_dsl import should, should_not
from nsi.metadataextractor.xml_parser import Parser
from nsi.metadataextractor.extractor import Preparator, TccExtractor

ROOT_PATH = abspath(dirname(__file__))
TEMPLATES_PATH = join(ROOT_PATH, '..', 'templates')

class TestPreparation(unittest.TestCase):

	def setUp(self):
		self.parse = Parser('tcc.xml')
		self.tipo = 'obtencaograu'
		self.nome = 'doctest1'
		self.preparator = Preparator(self.tipo, self.nome)
		
	def test_pdf_document_exists(self):
		self.obtencaograu_pdf_document = self.nome + '.pdf'
		self.obtencaograu_pdf_documents = listdir(join(ROOT_PATH, '..', 'articles', 'obtencaograu'))
		self.obtencaograu_pdf_document |should| be_into (self.obtencaograu_pdf_documents)
	
	def test_obtencao_grau_document_pdf_to_txt_convertion(self):
		self.converted_document = self.nome + '.txt'
		one_page_hash = self.parse.onepage_metadata
		page = one_page_hash['page']
		self.preparator.convert_document(page, page)
		self.obtecaograu_converted_documents = listdir(join(ROOT_PATH, '..', 'articles', 'obtencaograu', 'converted'))
		self.converted_document |should| be_into (self.obtecaograu_converted_documents)

	def test_name_corpus_has_a_certain_quantity_of_names(self):
		len(self.preparator.parse_corpus('names')) |should| equal_to(6287)

	def test_list_cleaner_cleans_document_lists(self):
		page = self.parse.onepage_metadata['page']
		document_list = self.preparator.convert_document(page, page)
		self.preparator.clean_document_list(document_list) |should_not| contain('\n')
		self.preparator.clean_document_list(document_list) |should_not| contain('.')

	def test_institution_corpus_is_a_list_of_institution_names_with_respective_prepositions(self):
		self.preparator.parse_corpus('institution') |should| equal_to(['de,Tocantins', 'do,Mato Grosso', 
			'do,Par\xc3\xa1', 'da,Para\xc3\xadba', 'de,Sergipe', 'do,Cear\xc3\xa1', 'de,Roraima', 
			'de,Alagoas', ',Catarinense', 'de,Santa Catarina', 'do,Sul de Minas', 'do,Sul de Minas Gerais', 'de,S\xc3\xa3o Paulo', 
			'do,Tri\xc3\xa2ngulo Mineiro', 'de,Minas Gerais', 'do,Sert\xc3\xa3o Pernambucano', 
			'do,Mato Grosso do Sul', ',Baiano', 'da,Bahia', 'de,Rondonia', 'do,Rio Grande do Sul', 
			'do,Rio Grande do Norte', 'de,Bras\xc3\xadlia', 'do,Norte de Minas', 'do,Piau\xc3\xad', 
			'de,Amazonas', 'do,Paran\xc3\xa1', 'de,Amap\xc3\xa1', 'do,Acre', 'de,Maranh\xc3\xa3o', 
			'do,Rio de Janeiro', 'de,Pernambuco', 'da,Bahia', 'do,Esp\xc3\xadrito Santo', ',Fluminense', 
			'do,Sudeste de Minas Gerais', ',Goiano', 'de,Goi\xc3\xa1s', 'de,Farroupilha', 'de,Goi\xc3\xa1s'])


class TestTccExtractor(unittest.TestCase):

	def setUp(self):
		self.nome = 'doctest1'
		self.extractor = TccExtractor(self.nome)

	def test_has_one_or_more_author_type_metadata_on_a_list(self):
		len(self.extractor.author_metadata()) |should| be_greater_than_or_equal_to(1)
		self.extractor.author_metadata() |should_not| contain('')


	def test_has_title_type_metadata(self):
		self.extractor.title_metadata() |should_not| equal_to('')

 	def test_institution_names_has_been_separated_from_prepositions(self):
 		self.extractor.institution_metadata()
 		self.extractor.institution_names |should| contain('tocantins')
 		self.extractor.institution_names |should| contain('goiás')
 		self.extractor.institution_prepositions |should| contain('da')
 		self.extractor.institution_prepositions |should| contain('de')
 		self.extractor.institution_prepositions |should| contain('do')

 		len(self.extractor.institution_names) |should| be_greater_than_or_equal_to(20)

 	def test_document_has_a_confirmed_by_corpus_institution_metadata(self):
 		self.extractor.institution_metadata() |should_not| equal_to('Instituto Federal de Educação Ciência e Tecnologia ')

 	def test_document_has_a_confirmed_by_corpus_campus_metadata(self):
 		self.extractor.campus_metadata() |should_not| equal_to('')

 	def test_document_has_abstract_metadata_type(self):
 		self.extractor.abstract_metadata()
 		doc = self.extractor.variouspages_doc
 		self.extractor.abstract_position |should| be_kind_of(int) 
 		self.extractor.abstract_metadata() |should| end_with('\n')


if __name__ == '__main__':
	unittest.main()

	

		
		