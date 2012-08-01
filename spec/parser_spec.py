#coding: utf-8
import os, sys, inspect
cmd_folder = '/Users/osw/nsi.metadataextractor/parser'
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

#################
import unittest
from should_dsl import should, should_not
from xml_parser import Parser
import nltk
import xml.etree.cElementTree as ET
##################

class TestParser(unittest.TestCase):

    def setUp(self):
        self.tccParse = Parser('tcc.xml')
        self.eventannalsParse = Parser('anais_evento.xml')

    def test_parser_has_a_xml_directory(self):
        self.tccParse.file_path |should| be_like(r'.*.xml')

    def test_onepage_metadata_has_a_valid_hash(self):
        type(self.tccParse.onepage_metadata) |should| equal_to(dict)

    def test_onepage_metadata_hash_has_valid_keys_and_values(self):
        metadata_hash = self.tccParse.onepage_metadata
        
        metadata_hash.get("campus_prefix") |should| equal_to (['CAMPUS', 'CAMPI'])
        metadata_hash.get("grau_doctoral") |should| equal_to (['DOUTORADO','DOUTOR'])
        metadata_hash.get("grau_graduation") |should| equal_to (['GRADUAÇÃO', 'CURSO SUPERIOR', 'BACHARELADO', 'LICENCIATURA', 'TECNÓLOGO'])
        metadata_hash.get("grau_master_degree") |should| equal_to (['MESTRADO', 'MESTRE'])
        metadata_hash.get("grau_postdoctoral") |should| equal_to (['PÓS-DOUTORADO', 'PÓS DOUTORADO'])
        metadata_hash.get("grau_spec") |should| equal_to (['PÓS-GRADUAÇÃO', 'LATO SENSU', 'ESPECIALIZAÇÃO', 'ESPECIALISTA', 'MBA'])
        metadata_hash.get("instituicao_prefix") |should| equal_to (['UNIVERSIDADE', 'INSTITUTO'])
        metadata_hash.get("page") |should| equal_to (2)
        metadata_hash.get("titulo_prefix") |should| equal_to (['\n'])

    def test_variouspages_metadata_has_a_valid_hash(self):
        type(self.tccParse.onepage_metadata) |should| equal_to(dict)

    def test_variouspages_metadata_hash_has_valid_keys_and_values(self):
        metadata_hash = self.tccParse.variouspages_metadata

        metadata_hash.get("resumo_position") |should| equal_to (1)
        metadata_hash.get("resumo_prefix") |should| equal_to (['RESUMO\n'])
        metadata_hash.get("pages") |should| equal_to ([1,10])


if __name__ == '__main__':
    unittest.main()