import re

ERR_LITERAL_CHAR = re.compile(r'\'[^\']*\'')

def get_error_info(_token):
  if ERR_LITERAL_CHAR.match(_token) != None:
    return '\nINFO: Literal character cannot be more than one character: {0}'.format(_token)
  
  else:
    return '\nINFO: The token is not part of UTF-32'