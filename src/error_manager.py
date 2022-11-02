import re

class ErrorManager(object):
  ERR_LITERAL_CHAR = re.compile(r'\'[^\']*\'')
  ERR_LITERAL_CHAR_WITHOUT_QUOTE = re.compile(r'[(\'.*)|(.*\')]')
  ERR_IDENTIFIER = re.compile(r'.*')
  ERR_STRING = re.compile(r'[(".*)|(.*")]')

  original_file = None
  file_lines = None
  token_list = None
  msg = ""

  def set_original_file(self,file_name):
    self.original_file = open(file_name,'r')
    self.file_lines = self.original_file.readlines()
    self.msg = "File {0} has errors".format(self.original_file.name)

  def __new__(cls, *args, **kwargs):
    if not hasattr(cls, 'instance'):
      cls.instance = super(ErrorManager, cls).__new__(cls)
    return cls.instance

  def get_syntax_error_message(self,token,_line_number=0):
    lines = self.file_lines
    error_position = lines[_line_number].find(token)

    self.msg += "\nInvalid syntax: In line {0}, position {1}\n".format(_line_number + 1, error_position + 1)
    self.msg += lines[_line_number].replace('\n','')
    self.msg += '\n' + ' ' * error_position + '^'
    return self.msg

  def get_lexical_error_message(self,token,_line_number=0):
    lines = self.file_lines
    error_position = lines[_line_number].find(token)

    self.msg += "\nIn line {0}, position {1} → Token {2} is not valid\n".format(_line_number + 1, error_position + 1, token)
    self.msg += lines[_line_number].replace('\n','')
    self.msg += '\n' + ' ' * error_position + '^'
    self.msg += self.get_lexical_error_info(token)
    return self.msg

  def get_lexical_error_info(self,_token):
    if self.ERR_LITERAL_CHAR.match(_token) != None:
      return '\nINFO: Literal character cannot be more than one character: {0}'.format(_token)
    elif self.ERR_LITERAL_CHAR_WITHOUT_QUOTE.match(_token) != None:
      return '\nINFO: Literal character must be between single quotes: {0}'.format(_token)
    elif self.ERR_STRING.match(_token) != None:
      return '\nINFO: Literal string must be between double quotes: {0}'.format(_token)
    elif self.ERR_IDENTIFIER.match(_token) != None:
      return '\nINFO: Invalid identifier. An ID must start with a letter and can only contain letters, numbers and underscores: {0}'.format(_token)
    
    else:
      return '\nINFO: The token is not part of UTF-32'