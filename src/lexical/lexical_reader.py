from src.custom_logger import CustomLogger
from src.error_manager import ErrorManager
from src.lexical.definitions import Definitions

from tabulate import tabulate
import re
import sys

clogger = CustomLogger(name='lexical_reader')
defs = Definitions()
error_manager = ErrorManager()

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

#! Función que cambia todas las variables de tipo _type_token y las remplazamos por una palabra reservada: _name
#! testeo = "perro caliente" -> testeo = TP_STRING
def replace_token_by_tory(_type_token, _line, _name = ""):
  line = _line
  token_list = _type_token.findall(line)
  for token in token_list:
    line = line.replace(token, _name)
    if _name != "":
      if _name.strip() not in defs.GL_LISTS:
        defs.GL_LISTS[_name.strip()] = []
      defs.GL_LISTS[_name.strip()].append(token)

  clogger.debug('Changing to {0}:'.format(_name.strip() if _name != "" else "BLANK if is a COMMENT")+' {0}'.format(line)) if token_list else None
  return line

environment = 0
defs.GL_ENVIRONMENT.append(environment)
def Get_tokens_list_from_line(line, _is_comment_block = False, _line_number = 0):  
  global environment
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
    line = replace_token_by_tory(defs.GL_COMPILERS[db_operator], line, ' TP_{0} '.format(defs.TEMP_RESERVED_WORDS[temp_key]))

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

  siguiente_en_tabla = False
  for token in temp_tokens:
    dict_value = token

    #! Identificamos si el token es un ID
    if defs.IDENTIFIER.match(token):
      if token in defs.GL_SYMBOL_TABLE:
        defs.GL_SYMBOL_TABLE[token]['references'].append(_line_number + 1)

      #! Identificamos si el token es una palabra reservada
      if token in defs.RESERVERD_WORDS:
        dict_token = defs.RESERVERD_WORDS[token]
        dict_number = defs.TOKEN_TYPES_INT[token]
        if token == 'var':
          siguiente_en_tabla = True
      #! Identificamos si el token es una palabra reservada temporal
      elif token in defs.TEMP_RESERVED_WORDS:
        if token == 'TP_STRING':
          value = []
          split_string = defs.GL_LISTS[token][0].split(' ')
          for string in split_string:
            if string in defs.GL_LISTS:
              new_string = defs.GL_LISTS[string][0]
              defs.GL_LISTS[string].pop(0)
              value.append(new_string)
            else:
              value.append(string)
          defs.GL_LISTS[token][0] = ' '.join(value)

        dict_token = defs.TOKEN_TYPES[defs.TEMP_RESERVED_WORDS[token]]
        dict_value = defs.GL_LISTS[token][0]
        dict_number = defs.TOKEN_TYPES_INT[defs.TOKEN_TYPES[defs.TEMP_RESERVED_WORDS[token]]]
        defs.GL_LISTS[token].pop(0)
      else:
        dict_token = defs.TOKEN_TYPES['TP_INDENTIFIER']
        dict_number = defs.TOKEN_TYPES_INT['ID']
        if siguiente_en_tabla:
          defs.GL_SYMBOL_TABLE[token] = {'type': 'VAR', 'environment': defs.GL_ENVIRONMENT[-1], 'line': _line_number + 1, 'references': []}
    #! Identificamos si el token es un numero
    elif defs.LITERA_INTEGER.match(token):
      dict_token = defs.TOKEN_TYPES['TP_INTEGER']
      dict_number = defs.TOKEN_TYPES_INT['LIIN']
    #! Identificamos si el token es un operador
    elif token in defs.OPERATORS:
      dict_token = defs.TOKEN_TYPES[defs.OPERATORS[token]]
      dict_number = defs.TOKEN_TYPES_INT[token]
    #! Identificamos si el token es un simbolo
    elif token in defs.SYMBOLS:
      dict_token = defs.TOKEN_TYPES[defs.SYMBOLS[token]]
      dict_number = defs.TOKEN_TYPES_INT[token]
      if token == ',' and siguiente_en_tabla:
        siguiente_en_tabla = True
      if token == '{':
        environment += 1
        defs.GL_ENVIRONMENT.append(environment)
      if token == '}':
        defs.GL_ENVIRONMENT.pop()
    else:
      msg = error_manager.get_lexical_error_message(token,_line_number)
      clogger.error(msg,'LEXICAL ERROR')
      clogger.without_format().info("")
      return [], False, True

    tokens_types.append({'token': dict_token, 'value': dict_value, 'number': dict_number, 'line': _line_number})

  clogger.debug("Resulting tokens: " + str(tokens_types))

  clogger.print_break_line()
  return tokens_types, is_comment_block, False

def Get_tokens_list_from_file(file_name, debug_mode = False, test_mode = False):
  global error_manager
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
    error_manager.set_original_file(file_name)
    clogger.print_break_line()
    defs.custom_init()
    
    clogger.debug("New reserved words list: {0}".format(defs.TEMP_RESERVED_WORDS))
    
    temp = []
    for token_type_int in defs.TOKEN_TYPES:
      temp.append([token_type_int,defs.TOKEN_TYPES[token_type_int]])
    clogger.debug("\nNew token types list:\n{0}".format(tabulate(temp, headers=['Token', 'Value'], showindex="always", tablefmt="pretty")))

    temp = []
    for token_type_int in defs.TOKEN_TYPES_INT:
      temp.append([token_type_int,defs.TOKEN_TYPES_INT[token_type_int]])
    clogger.debug("\nNew token types int list:\n{0}".format(tabulate(temp, headers=['Token', 'INT'], showindex="always", tablefmt="pretty")))

    clogger.print_break_line()

    tokens = []
    is_comment_block = False
    line_number = 0
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

      for dfsymbol in defs.GL_SYMBOL_TABLE:
        defs.GL_SYMBOL_TABLE[dfsymbol]['references'] = list(set(defs.GL_SYMBOL_TABLE[dfsymbol]['references']))

      for defsasa in defs.GL_SYMBOL_TABLE:
        print(defsasa, defs.GL_SYMBOL_TABLE[defsasa])
    return definitions

  else:
    clogger.error("({0}) File type not supported. Only .quetzal files are supported".format(file_name))
    return