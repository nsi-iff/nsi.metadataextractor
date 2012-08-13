#coding: utf-8
import xml.etree.cElementTree as ET
from os import path

class Parser(object):

    def __init__(self, template_name):
        self.template_name = template_name
        self.file_path = path.join(path.abspath('app/templates'), self.template_name)
        self.doc = ET.ElementTree(file = self.file_path)
        
    @property
    def onepage_metadata(self):
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
		
    @property
    def variouspages_metadata(self):
        self.variouspages_dict = {}
        pages_parse = [(int(self.doc.find('VariousPages').attrib['startpage'])), (int(self.doc.find('VariousPages').attrib['endpage']))]
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