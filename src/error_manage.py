import re

ERR_LITERAL_CHAR = re.compile(r'\'[^\']*\'')
ERR_LITERAL_CHAR_WITHOUT_QUOTE = re.compile(r'[(\'.*)|(.*\')]')
ERR_IDENTIFIER = re.compile(r'.*')
ERR_STRING = re.compile(r'[(".*)|(.*")]')

def get_error_info(_token):
  if ERR_LITERAL_CHAR.match(_token) != None:
    return '\nINFO: Literal character cannot be more than one character: {0}'.format(_token)
  elif ERR_LITERAL_CHAR_WITHOUT_QUOTE.match(_token) != None:
    return '\nINFO: Literal character must be between single quotes: {0}'.format(_token)
  elif ERR_STRING.match(_token) != None:
    return '\nINFO: Literal string must be between double quotes: {0}'.format(_token)
  elif ERR_IDENTIFIER.match(_token) != None:
    return '\nINFO: Invalid identifier. An ID must start with a letter and can only contain letters, numbers and underscores: {0}'.format(_token)
  
  else:
    return '\nINFO: The token is not part of UTF-32'