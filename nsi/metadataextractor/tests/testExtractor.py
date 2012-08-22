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
		self.parse = Parser(join(TEMPLATES_PATH, 'tcc.xml'))
		self.tipo = 'obtencaograu'
		self.nome = '1'
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
		len(self.preparator.parse_corpus('names')) |should| equal_to(1639)

	def test_institution_corpus_is_a_list_of_institution_names(self):
		self.preparator.parse_corpus('institution') |should| equal_to(['Tocantins', 'Mato Grosso', 
			'Par\xc3\xa1', 'Para\xc3\xadba', 'Sergipe', 'Cear\xc3\xa1', 'Roraima', 'Alagoas', 
			'Catarinense', 'Sul de Minas', 'S\xc3\xa3o Paulo', 'Tri\xc3\xa2ngulo Mineiro', 
			'Minas Gerais', 'Sert\xc3\xa3o Pernambucano', 'Mato Grosso do Sul', 'Baiano', 
			'Bahia', 'Rondonia', 'Rio Grande do Sul', 'Rio Grande do Norte', 'Bras\xc3\xadlia', 
			'Norte de Minas', 'Piau\xc3\xad', 'Amazonas', 'Paran\xc3\xa1', 'Amap\xc3\xa1', 'Acre', 
			'Maranh\xc3\xa3o', 'Rio de Janeiro', 'Pernambuco', 'Bahia', 'Esp\xc3\xadrito Santo', 
			'Santa Catarina', 'Fluminense', 'Sudeste de Minas Gerais', 'Goiano', 'Goi\xc3\xa1s', 
			'Farroupilha', 'Goi\xc3\xa1s'])


class TestTccExtractor(unittest.TestCase):

	def setUp(self):
		self.extractor = TccExtractor('1')

	def test_has_one_or_more_author_type_metadata(self):
		len(self.extractor.author_metadata()) |should| be_greater_than_or_equal_to(3)

	def test_has_title_type_metadata(self):
		self.extractor.title_metadata() |should| equal_to('INTEGRAÇÃO DA GERÊNCIA DE REQUISITOS COM A PLATAFORMA REDMINE ')

 
if __name__ == '__main__':
	unittest.main()

	

		
		