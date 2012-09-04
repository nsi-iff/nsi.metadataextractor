import argparse
import sys
from json import dumps

from nsi.metadataextractor.extractor import TccExtractor

def set_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("document", type=str, help="Path of the document to extract metadata")
	parser.add_argument("-t", "--type", type=str, help="Type of the document", default="tcc")
	return parser

def parse_args(parser):
	return parser.parse_args()

def main(args=sys.argv):
	parser = set_args()
	args = parse_args(parser)
	if args.type == 'tcc':
		extractor = TccExtractor(args.document)
		metadata = extractor.all_metadata()
		print dumps(metadata)