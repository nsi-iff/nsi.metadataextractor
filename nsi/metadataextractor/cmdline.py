import argparse
import sys
from json import dumps

# Extractors
from nsi.metadataextractor.extractors.tcc import TccExtractor
from nsi.metadataextractor.extractors.event import EventExtractor
from nsi.metadataextractor.extractors.periodic import PeriodicExtractor

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
	extractors = {"tcc": TccExtractor(args.document),
	"event": EventExtractor(args.document),
	"periodic": PeriodicExtractor(args.document)}
	extractor = extractors[args.type]
	metadata = extractor.all_metadata()
	print dumps(metadata)