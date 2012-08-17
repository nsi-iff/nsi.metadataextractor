#coding: utf-8
#### RUBY CODE ###
#require File.expand_path(__FILE__ + '/../../' + 'lib/extractor')

#class EventAnnalsExtractor < Extractor
  
#  attr_reader :page, :one_page_pattern, :first_line, :last_line

#  def initialize(doc_type = "AnaisEvento", doc_name)
#  	parse = Parser.new(doc_type)
#  	@extractor = Extractor.new(doc_type, doc_name)
#    hash = parse.access_xml
#    @page = hash['root']['OnePage']['page'].to_i
#    @one_page_pattern = hash['root']['OnePage']['metadata'].first
#    
#  end
#  
#  def extract_abstract_metadata
#	  prefixes = @one_page_pattern['prefix'].split(',')
#	  suffixes = @one_page_pattern['suffix'].split(',')
#	  document = @extractor.convert_document(@page, @page)
#	  document_lines = list_upcase(document.readlines) - WHITESPACE
#
#   section = []
#
#    document_lines.each_index do |line|
#      case document_lines[line]
#      when /RESUM[O. ]/
#        section.push document_lines[line]
#        p "passou"
#        next
#      when /PALAVRAS.CHAVE/
#        break
#      end    
#    end
#    print section
#  end
  	
#end