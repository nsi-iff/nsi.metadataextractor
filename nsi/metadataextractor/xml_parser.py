#coding: utf-8
from lxml.etree import ElementTree
from os.path import abspath, dirname, join

ROOT_PATH = abspath(dirname(__file__))
TEMPLATE_PATH = join(ROOT_PATH, 'templates')

class Parser(object):

    def __init__(self, template_name):
        self.template_name = template_name
        self.file_path = join(TEMPLATE_PATH, self.template_name)
        self.doc = ElementTree(file = self.file_path)
        
    def _onepage_metadata(self):
        self.onepage_dict = {}	
        page = {'page': int(self.doc.find('OnePage').attrib['page'])}
        self.onepage_dict.update(page)
        for elem in self.doc.iterfind('OnePage/metadata'):
            for sub_elem in list(elem):
                key = elem.attrib['id'] + '_' + sub_elem.tag
                value = sub_elem.text.encode('utf-8')
                if value.isdigit():
                    value = int(value)
                elif '\\n' in value:
                    value = value.replace('\\n', '\n').split(',')
                else:
                    value = value.split(',')
                self.onepage_dict.update({key: value})
        return self.onepage_dict
		
    def _variouspages_metadata(self):
        self.variouspages_dict = {}
        various_pages = self.doc.find('VariousPages')
        if various_pages is not None:
            first_page = int(self.doc.find('VariousPages').attrib['startpage'])
            end_page = int(self.doc.find('VariousPages').attrib['endpage'])
            pages_parse = [first_page, end_page]
            pages = {'pages': pages_parse}
            self.variouspages_dict.update(pages)
            for elem in self.doc.iterfind('VariousPages/metadata'):
                for sub_elem in list(elem):
                    key = elem.attrib['id'] + '_' + sub_elem.tag
                    value = sub_elem.text.encode('utf-8')
                    if value.isdigit():
                        value = int(value)
                    elif '\\n' in value:
                        value = value.replace('\\n', '\n').split(',')
                    else:
                        value = value.split(',')    
                    self.variouspages_dict.update({key: value})
        return self.variouspages_dict

    def xml_template_metadata(self):
        onepage_metadata = self._onepage_metadata()
        variouspages_metadata = self._variouspages_metadata()
        onepage_metadata.update(variouspages_metadata)
        all_template_metadata = onepage_metadata
        return all_template_metadata
