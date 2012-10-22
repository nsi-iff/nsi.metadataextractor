#coding: utf-8
from os import listdir
from os.path import abspath, dirname, join
from nsi.metadataextractor.xml_parser import Parser
import unittest
from should_dsl import should, should_not


ROOT_PATH = abspath(dirname(__file__))
TEMPLATE_PATH = join(ROOT_PATH, '..', 'templates')

class TestParser(unittest.TestCase):

    def setUp(self):
        self.tccParse = Parser(join(TEMPLATE_PATH, 'tcc.xml'))
        self.eventParse = Parser(join(TEMPLATE_PATH, 'event.xml'))

    def test_parser_receive_a_xml_directory(self):
        self.tccParse.file_path and self.eventParse.file_path |should| be_like(r'.*.xml')

    def tes_tcc_onepage_metadata_hash_has_valid_keys_and_values(self):
        onepage_parser = self.tccParse._onepage_metadata() 
        "author_residue", "institution_validator", "campus_validator",
        "grade_graduation", "grade_spec", "grade_master_degree", "grade_doctoral" 
        "grade_postdoctoral" |should| be_into(onepage_parser.keys())
        for key in onepage_parser.keys():
            onepage_parser.get(key) |should_not| equal_to ([])

    def test_event_onepage_metadata_hash_has_valid_keys_and_values(self):
        onepage_parser = self.tccParse._onepage_metadata() 
        "author_breaker", "author_residue", "title_breaker" |should| be_into(onepage_parser.keys())
        for key in onepage_parser.keys():
            onepage_parser.get(key) |should_not| equal_to ([])

    def test_tcc_variouspages_metadata_hash_has_valid_keys_and_values(self):
        variouspages_parser = self.tccParse._variouspages_metadata()
        "pages" |should| be_into(variouspages_parser.keys()) 
        
    def test_merge_all_template_metadata_into_one_dict(self):
        onepage_metatada = self.tccParse._onepage_metadata()
        variouspages_metatada = self.tccParse._variouspages_metadata()
        xml_template_metadata = self.tccParse.xml_template_metadata()
        xml_template_metadata.keys() |should_not| be_empty


if __name__ == '__main__':
    unittest.main()