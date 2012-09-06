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
        self.eventannalsParse = Parser(join(TEMPLATE_PATH, 'anais_evento.xml'))

    def test_parser_has_a_xml_directory(self):
        self.tccParse.file_path |should| be_like(r'.*.xml')

    def test_onepage_metadata_has_a_valid_hash(self):
        type(self.tccParse._onepage_metadata()) |should| equal_to(dict)

    def test_onepage_metadata_hash_has_valid_keys_and_values(self):
        onepage_metatada = self.tccParse._onepage_metadata()
        
        onepage_metatada.get("author_position") |should| equal_to (0)
        onepage_metatada.get("author_sucessor") |should| equal_to (['\n'])
        onepage_metatada.get("campus_validator") |should| equal_to (['campus', 'campi'])
        onepage_metatada.get("grade_doctoral") |should| equal_to (['doutorado','doutor'])
        onepage_metatada.get("grade_graduation") |should| equal_to (['graduação', 'curso superior', 'bacharelado', 
            'licenciatura', 'tecnólogo'])
        onepage_metatada.get("grade_master_degree") |should| equal_to (['mestrado', 'mestre'])
        onepage_metatada.get("grade_postdoctoral") |should| equal_to (['pós doutorado', 'pós-doutorado'])
        onepage_metatada.get("grade_spec") |should| equal_to (['pós-graduação','lato sensu','especialização',
            'especialista','mba'])
        onepage_metatada.get("institution_validator") |should| equal_to (['universidade', 'instituto'])
        onepage_metatada.get("page") |should| equal_to (2)
        onepage_metatada.get("title_antecessor") |should| equal_to (['\n'])
        onepage_metatada.get("title_sucessor") |should| equal_to (['\n'])
        onepage_metatada.get("title_breaker") |should| equal_to (['monografia'])
        onepage_metatada.get("author_residue") |should| equal_to (['orientador', 'orientadora', 'co-orientador', 
            'co-orientadora', 'prof.', 'profa.', 'reitora:', 'pr\xc3\xb3-reitora:', 'reitora', 'pr\xc3\xb3-reitora', 
            'dra.', 'dr.', 'instituto', 'universidade'])

    def test_variouspages_metadata_has_a_valid_hash(self):
        type(self.tccParse._onepage_metadata()) |should| equal_to(dict)

    def test_variouspages_metadata_hash_has_valid_keys_and_values(self):
        variouspages_metatada = self.tccParse._variouspages_metadata()

        variouspages_metatada.get("abstract_antecessor") |should| equal_to (['RESUMO\n'])
        variouspages_metatada.get("abstract_sucessor") |should| equal_to (['\n'])
        variouspages_metatada.get("pages") |should| equal_to ([4, 10])

    def test_merge_all_template_metadata_into_one_dict(self):
        onepage_metatada = self.tccParse._onepage_metadata()
        variouspages_metatada = self.tccParse._variouspages_metadata()
        xml_template_metadata = self.tccParse.xml_template_metadata()
        xml_template_metadata.keys() |should| equal_to(['grade_postdoctoral', 'title_antecessor', 
            'author_residue', 'grade_master_degree', 'abstract_antecessor', 'grade_graduation', 
            'institution_validator', 'pages', 'campus_validator', 'author_position', 'title_sucessor', 
            'abstract_sucessor', 'author_sucessor', 'grade_spec', 'grade_doctoral', 'page', 'title_breaker'])


if __name__ == '__main__':
    unittest.main()