class TccExtractor():

  def extract_authors
    authors = []
    convert_document(@page, @page+1)
    document_lines = @document.readlines
    first_author = document_lines.first == "\n" ? 1 : 0 #Starting document line
    document_lines.each_index do |author_index|    
      if document_lines[author_index] != "\n"
        authors << document_lines[author_index].strip
      else
        @last_author_line = author_index + 1
        break
      end 
    end
    authors
  end

  def extract_title
    metadata = @xmlobject.find_title
    title = " "
    convert_document(@page, @page)
    document_lines = @document.readlines
    title_starting_index = @last_author_line
    while document_lines[title_starting_index] != "\n"
      title += document_lines[title_starting_index]
      title_starting_index += 1
    end
  title.strip.gsub("\n",' ')
  end

  def extract_abstract
    summary = []
    start_index = 1
    metadata = @xmlobject.find_abstract
    word = metadata[1] #RESUMO\n
    (@pages[0]..@pages[1]).each do |loop|
      convert_document(loop, loop+1)
      document_lines = @document.readlines
      if document_lines[0] == word
        if document_lines[start_index] == "\n"
          start_index += 1
        end

        while document_lines[start_index] != "\n" do
          summary << document_lines[start_index]
            start_index += 1
          end
        end

        if not summary.empty?
          break
        end
      end
      #concatenate and remove \\n
  summary = (summary * '').gsub("\n",' ')
  end

  def extract_institution
    result = ''
    metadata = @xmlobject.find_institution
    convert_document(@page, @page)
    document_lines = list_upcase(@document.readlines)
    metadata.each_index do |loop|
      document_lines.each_index do |index|
        if document_lines[index].include? (metadata[loop]) and result == ''
          result = (document_lines[index] + document_lines[index+1] + document_lines[index+2])
        elsif result != ''
          break
        end
      end
    end
    #Catch the line that includes metadata[loop], and the next 2 lines.
    result = (result.gsub(",",'').split - STOP_WORDS) - EXTRA_STOP_WORDS
  end

  def search_institution_file
    institution_data = ''
    institution = extract_institution
    inst_list = list_upcase(File.open(File.expand_path(__FILE__ + '/../../' + "data/Instituto.txt")).readlines)
    biggest_length = 0
    #Run into institution list spliting till catch only the institution name.
    #The loop compares and returns the biggest length using &. The biggest length on
    #the extracted "tags" (institution) & institution name, must be our guy.
    inst_list.each_index do |index|
      splited_list = inst_list[index].split(",")
      institution_name = (splited_list[2][25,splited_list[2].length].split(' ')) - EXTRA_STOP_WORDS
      equal_name = (institution & institution_name).length
      if equal_name > biggest_length
        biggest_length = equal_name
        institution_data = inst_list[index]
      end
    end
  institution_data.strip
  end

  def extract_campus
    document_result = ''
    metadata = @xmlobject.find_campus
    convert_document(@page, @page)
    document_lines = list_upcase(@document.readlines)
    metadata.each_index do |template_index|
      document_lines.each_index do |line_index|
        if document_lines[line_index].include? (metadata[template_index])
          document_result = (document_lines[line_index] + document_lines[line_index+1])
          break
        end
      end
    end
  document_result = document_result.gsub(",",'').split - STOP_WORDS
  end


  def search_campi_file
    campus_data = 'Campus '
    campus = extract_campus
    campus_list = list_upcase(File.open('data/Campus.txt').readlines)
    #Run into institution list, upcasing and spliting till catch only the institution name.
    #It returns what's equal on metadata extraction (institution) and (inst_list),
    #finding the right line on "Instituto" archive.
    campus_list.each_index do |index|
      splited_list = campus_list[index].split(",")
      campus_name = splited_list[1].split(' ') - STOP_WORDS
      equal_name = campus_name & campus
      if equal_name == campus_name
        campus_data += equal_name * ' '
        break
      end
    end
    if campus_data != 'Campus '
      return campus_data
    else
      return "Campus não encontrado."
    end
  end

  def extract_grade
    graduation_level = '' 
    spec_level = ''
    masterdegree_level = '' 
    doctoral_level = ''   
    postdoctoral_level = ''
    big_string = ''
    
    graduation_metadata = @xmlobject.find_graduation
    spec_metadata = @xmlobject.find_specialization
    masterdegree_metadata = @xmlobject.find_masterdegree
    doctoral_metadata = @xmlobject.find_doctoral
    postdoctoral_metadata = @xmlobject.find_postdoctoral

    convert_document(@page, @page)
    document_lines = list_upcase(@document.readlines)

    document_lines.each do |line|
      big_string += line.gsub("\n", " ")
    end
         
    graduation_metadata.each do |graduation|
      if big_string.include? graduation
        graduation_level = GRADUATION
      end
    end

    spec_metadata.each do |spec|
      if big_string.include? spec
        spec_level = SPECIALIZATION
      end
    end

    masterdegree_metadata.each do |master_degree|
      if big_string.include? master_degree
        masterdegree_level = MASTERDEGREE
      end
    end

    doctoral_metadata.each do |doctoral|
      if big_string.include? doctoral
        doctoral_level = DOCTORAL
      end
    end

    postdoctoral_metadata.each do |postdoctoral|
      if big_string.include? postdoctoral
        postdoctoral_level = POSTDOCTORAL
      end
    end

    return postdoctoral_level unless postdoctoral_level.empty?
    return doctoral_level unless doctoral_level.empty?
    return masterdegree_level unless masterdegree_level.empty?
    return spec_level unless spec_level.empty?
    return graduation_level unless graduation_level.empty?
  end
