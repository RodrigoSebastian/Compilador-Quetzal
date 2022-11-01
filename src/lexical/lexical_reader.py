from src.custom_logger import CustomLogger
import src.lexical.definitions as defs
from tabulate import tabulate
import re
import sys
import src.error_manage as err

clogger = CustomLogger(name='lexical_reader')

GL_LISTS = {}
GL_COMPILERS = {}

#! Funcion para imprimir la tabla de simbolos
def print_tokens(definitions):
  only_for_print = []
  for definition in definitions:
    temp = []
    temp.append(definition['token'])
    temp.append(definition['value'])
    temp.append(definition['number'])
    only_for_print.append(temp)
  
  clogger.without_format().debug(tabulate(only_for_print, headers=['Token', 'Valor', 'Token_INT'], showindex="always", tablefmt="pretty"))

#! Funcion para inicializar las variables globales
def important_initialization():
  for db_operator in defs.DB_OPERATORS:
    if db_operator not in GL_COMPILERS:
      GL_COMPILERS[db_operator] = re.compile(r'{0}'.format(db_operator))
    if 'TP_{0}'.format(defs.DB_OPERATORS[db_operator]) not in defs.TEMP_RESERVED_WORDS:
      defs.TEMP_RESERVED_WORDS['TP_{0}'.format(defs.DB_OPERATORS[db_operator])] = defs.DB_OPERATORS[db_operator]

  clogger.debug("New reserved words list: {0}".format(defs.TEMP_RESERVED_WORDS))

  amount_tokens = len(defs.TOKEN_TYPES_INT)
  for element in defs.SYMBOLS:
    defs.TOKEN_TYPES[defs.SYMBOLS[element]] = element
    defs.TOKEN_TYPES_INT[element] = amount_tokens
    amount_tokens += 1

  amount_tokens = len(defs.TOKEN_TYPES_INT)
  for element in defs.RESERVERD_WORDS:
    defs.TOKEN_TYPES_INT[defs.RESERVERD_WORDS[element]] = amount_tokens
    amount_tokens += 1

  amount_tokens = len(defs.TOKEN_TYPES_INT)
  for element in defs.OPERATORS:
    defs.TOKEN_TYPES[defs.OPERATORS[element]] = element
    defs.TOKEN_TYPES_INT[element] = amount_tokens
    amount_tokens += 1

  amount_tokens = len(defs.TOKEN_TYPES_INT)
  for element in defs.DB_OPERATORS:
    defs.TOKEN_TYPES[defs.DB_OPERATORS[element]] = element
    defs.TOKEN_TYPES_INT[element] = amount_tokens
    amount_tokens += 1

  temp = []
  for token_type_int in defs.TOKEN_TYPES:
    temp.append([token_type_int,defs.TOKEN_TYPES[token_type_int]])
  clogger.debug("New token types list:\n{0}".format(tabulate(temp, headers=['Token', 'Value'], showindex="always", tablefmt="pretty")))

  temp = []
  for token_type_int in defs.TOKEN_TYPES_INT:
    temp.append([token_type_int,defs.TOKEN_TYPES_INT[token_type_int]])
  clogger.debug("New token types int list:\n{0}".format(tabulate(temp, headers=['Token', 'INT'], showindex="always", tablefmt="pretty")))

  clogger.print_break_line()

#! Función que cambia todas las variables de tipo _type_token y las remplazamos por una palabra reservada: _name
#! testeo = "perro caliente" -> testeo = TP_STRING
def replace_token_by_tory(_type_token, _line, _name = ""):
  line = _line
  token_list = _type_token.findall(line)
  for token in token_list:
    line = line.replace(token, _name)
    if _name != "":
      if _name.strip() not in GL_LISTS:
        GL_LISTS[_name.strip()] = []
      GL_LISTS[_name.strip()].append(token)

  clogger.debug('Changing to {0}:'.format(_name.strip() if _name != "" else "BLANK if is a COMMENT")+' {0}'.format(line)) if token_list else None
  return line

def Get_tokens_list_from_line(line, _is_comment_block = False, line_number = 0):
  original_line = line
  is_comment_block = _is_comment_block

  if line == '\n':                                     #! Si la linea esta vacia, no hacer nada
    return [], is_comment_block, False

  if(len(defs.END_COMMENT_BLOCK.findall(line)) > 0):   #! Verifica si la linea es un fin de bloque de comentario
    is_comment_block = False

  if is_comment_block:                                 #! Si es un bloque de comentario, no se hace nada
    return [], is_comment_block, False

  line = line.strip('\n')                              #! Elimina los saltos de linea
  clogger.debug("Reading line: "+ line)

  #! Reemplazamos los caracteres speciales por un token
  line = replace_token_by_tory(defs.LITERAL_ESCAPED_CHAR, line, ' TP_ES_CHAR ')
  #! Reemplazamos los caracteres unicode por un token
  line = replace_token_by_tory(defs.LITERAL_UNICODE_CHAR, line, ' TP_UC_CHAR ')
  #! Reemplazamos los caracteres por un token
  line = replace_token_by_tory(defs.LITERAL_CHAR, line, ' TP_CHAR ')
  #! Reemplazamos los strings por un token
  line = replace_token_by_tory(defs.LITERAL_STRING, line, ' TP_STRING ')
  
  #! Quitamos todos los comentarios existentes en la linea
  line = replace_token_by_tory(defs.COMMENT, line) 
  line = replace_token_by_tory(defs.COMMENT_BLOCK, line)
  if(len(defs.START_COMMENT_BLOCK.findall(line)) > 0): #! Si la linea tiene un inicio de bloque de comentarios entonces
    is_comment_block = True                            #! se activa el modo de bloque de comentarios ignorando todas las
                                                       #! demás lineas hasta que se encuentre un fin de bloque de comentarios
  line = replace_token_by_tory(defs.START_COMMENT_BLOCK, line)
  line = replace_token_by_tory(defs.END_COMMENT_BLOCK, line)

  for db_operator in defs.DB_OPERATORS:                #! Reemplazamos los operadores dobles por un token
    temp_key = 'TP_{0}'.format(defs.DB_OPERATORS[db_operator])
    line = replace_token_by_tory(GL_COMPILERS[db_operator], line, ' TP_{0} '.format(defs.TEMP_RESERVED_WORDS[temp_key]))

  clogger.debug("Line after replacing words: " + line.strip('\n'))

  #! Separamos toda nuestra linea de entrada por espacios para empezar a separar por tokens
  #! print(perro caliente) -> ['print(perro', 'caliente)']
  temp_tokens = []
  tokens_types = []
  temp_split_line = line.split(' ')
  split_line = [token for token in temp_split_line if token != '']

  clogger.debug("Line after splitting: " + str(split_line))

  #! Separamos todos los tokens por caracteres especiales
  #! ['print(perro', 'caliente)'] -> ['print', '(', 'perro', 'caliente', ')']
  for token in split_line:
    temp_tokens.append(re.split(r'([,.;:=+(){}[\]/|<>!#@$%^&*~"`]|:?\\+|-)', token))
  temp_tokens = [item for sublist in temp_tokens for item in sublist if item]
  temp_tokens = [token for token in temp_tokens if token != '\n']
  
  clogger.debug("Line after splitting by punctuation: " + str(temp_tokens))

  for token in temp_tokens:
    #! Identificamos si el token es un ID
    if defs.IDENTIFIER.match(token):
      #! Identificamos si el token es una palabra reservada
      if token in defs.RESERVERD_WORDS:
        tokens_types.append({'token': defs.RESERVERD_WORDS[token], 'value': token, 'number': defs.TOKEN_TYPES_INT[token]})
      #! Identificamos si el token es una palabra reservada temporal
      elif token in defs.TEMP_RESERVED_WORDS:
        if token == 'TP_STRING':
          value = []
          split_string = GL_LISTS[token][0].split(' ')
          for string in split_string:
            if string in GL_LISTS:
              new_string = GL_LISTS[string][0]
              GL_LISTS[string].pop(0)
              value.append(new_string)
            else:
              value.append(string)
          GL_LISTS[token][0] = ' '.join(value)

        tokens_types.append({'token': defs.TOKEN_TYPES[defs.TEMP_RESERVED_WORDS[token]], 'value': GL_LISTS[token][0], 'number': defs.TOKEN_TYPES_INT[defs.TOKEN_TYPES[defs.TEMP_RESERVED_WORDS[token]]]})
        GL_LISTS[token].pop(0)
      else:
        tokens_types.append({'token': defs.TOKEN_TYPES['TP_INDENTIFIER'], 'value': token, 'number': defs.TOKEN_TYPES_INT['ID']})
    #! Identificamos si el token es un numero
    elif defs.LITERA_INTEGER.match(token):
      tokens_types.append({'token': defs.TOKEN_TYPES['TP_INTEGER'], 'value': token, 'number': defs.TOKEN_TYPES_INT['LIIN']})
    #! Identificamos si el token es un operador
    elif token in defs.OPERATORS:
      tokens_types.append({'token': defs.TOKEN_TYPES[defs.OPERATORS[token]], 'value': token, 'number': defs.TOKEN_TYPES_INT[token], 'number': defs.TOKEN_TYPES_INT[token]})
    #! Identificamos si el token es un simbolo
    elif token in defs.SYMBOLS:
      tokens_types.append({'token': defs.TOKEN_TYPES[defs.SYMBOLS[token]], 'value': token, 'number': defs.TOKEN_TYPES_INT[token]})
    else:
      error_position = original_line.find(token) + 1
      token = token.strip('\n')
      msg = "In line {0}, position {1} → Token {2} is not valid{3}".format(line_number, error_position, token, err.get_error_info(token))
      clogger.error(msg,'LEXICAL ERROR')
      clogger.without_format().info("")
      return [], False, True

  clogger.debug("Resulting tokens: " + str(tokens_types))

  clogger.print_break_line()
  return tokens_types, is_comment_block, False

def Get_tokens_list_from_file(file_name, debug_mode = False, test_mode = False):
  clogger.without_format().info("")
  clogger.one_line().info("Starting Quetzal compiler...")
  if debug_mode:
    clogger.one_line().info("Debug mode activated. The compiler will show more information about the process")

  clogger.setLevel('DEBUG') if debug_mode else clogger.setLevel('INFO')

  file_type = file_name.split(".")[-1]
  if file_type == "quetzal":
    file = open(file_name, "r")

    clogger.one_line().info("Reading file: " + file_name)
    file_lines = file.readlines()
    clogger.print_break_line()
    important_initialization()

    tokens = []
    is_comment_block = False
    line_number = 1
    error = False
    definitions = []
    for line in file_lines:
      temp_tokens, is_comment_block, error = Get_tokens_list_from_line(line, is_comment_block, line_number)
      if error:
        if test_mode:
          break;
        sys.exit(1)
      tokens.append(temp_tokens)
      line_number += 1
    
    if error == False:
      definitions = [item for sublist in tokens for item in sublist]

      print_tokens(definitions)
      clogger.print_break_line()
      
      clogger.one_line().info('Lexical: File is splitted in tokens')
    return definitions

  else:
    clogger.error("({0}) File type not supported. Only .quetzal files are supported".format(file_name))
    return