from ast import Return
import definitions as defs
import logging
import os
import re

#! Create log_info folder if it doesn't exist
os.mkdir('log_info') if not os.path.exists('log_info') else None

#! Configure logger to manage errors and warnings
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_formatter = logging.Formatter('%(asctime)s:%(levelname)s:\n\t%(message)s')
stream_formatter = logging.Formatter('\033[92m'+'%(asctime)s:%(levelname)s:'+'\033[0m'+'\n\t%(message)s')

file_handler = logging.FileHandler('log_info/lexical_reader.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(file_formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(stream_formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

GL_LISTS = {}

def print_break_line():
  stream_handler.setFormatter(logging.Formatter('%(message)s'))
  file_handler.setFormatter(logging.Formatter('%(message)s'))
  logger.debug("=====================================================================")
  file_handler.setFormatter(file_formatter)
  stream_handler.setFormatter(stream_formatter)

def replace_token_by_tory(_type_token, _line, _name = ""):
  line = _line
  token_list = _type_token.findall(line)
  for token in token_list:
    line = line.replace(token, _name)
    if _name != "":
      if _name.strip() not in GL_LISTS:
        GL_LISTS[_name.strip()] = []
      GL_LISTS[_name.strip()].append(token)

  logger.debug('Changing to {0}:'.format(_name.strip() if _name != "" else "BLANK if is a COMMENT")+' {0}'.format(line)) if token_list else None
  return line

def Get_tokens_list_from_line(line, _is_comment_block = False):
  is_comment_block = _is_comment_block

  if line == '\n':                                     #! Si la linea esta vacia, no hacer nada
    return [], is_comment_block

  if(len(defs.END_COMMENT_BLOCK.findall(line)) > 0):   #! Verifica si la linea es un fin de bloque de comentario
    is_comment_block = False

  if is_comment_block:                                 #! Si es un bloque de comentario, no se hace nada
    return [], is_comment_block

  logger.debug("Reading line: "+ line.strip('\n'))

  #! Reemplazamos los strings por un token
  line = replace_token_by_tory(defs.LITERAL_STRING, line, ' TP_STRING ')
  #! Reemplazamos los caracteres por un token
  line = replace_token_by_tory(defs.LITERAL_CHAR, line, ' TP_CHAR ')
  
  #! Quitamos todos los split_linecomentarios existentes en la linea
  line = replace_token_by_tory(defs.COMMENT, line) 
  if(len(defs.START_COMMENT_BLOCK.findall(line)) > 0): #! Si la linea tiene un inicio de bloque de comentarios entonces
    is_comment_block = True                            #! se activa el modo de bloque de comentarios ignorando todas las
                                                       #! demás lineas hasta que se encuentre un fin de bloque de comentarios
  line = replace_token_by_tory(defs.START_COMMENT_BLOCK, line)
  line = replace_token_by_tory(defs.END_COMMENT_BLOCK, line)
  line = replace_token_by_tory(defs.COMMENT_BLOCK, line)

  logger.debug("Line after replacing words: " + line.strip('\n'))

  #! Separamos toda nuestra linea de entrada por espacios para empezar a separar por tokens
  #! print(perro caliente) -> ['print(perro', 'caliente)']
  temp_tokens = []
  tokens_types = []
  temp_split_line = line.split(' ')
  split_line = [token for token in temp_split_line if token != '']

  logger.debug("Line after splitting: " + str(split_line))

  #! Separamos todos los tokens por caracteres especiales
  #! ['print(perro', 'caliente)'] -> ['print', '(', 'perro', 'caliente', ')']
  for token in split_line:
    temp_tokens.append(re.split(r'([,.;:=+(){}[\]/|<>!#@$%^&*~"`]|:?\\+|-)', token))
  temp_tokens = [item for sublist in temp_tokens for item in sublist if item]
  temp_tokens = [token for token in temp_tokens if token != '\n']
  
  logger.debug("Line after splitting by punctuation: " + str(temp_tokens))

  for token in temp_tokens:
    #! Identificamos si el token es un ID
    if defs.IDENTIFIER.match(token):
      #! Identificamos si el token es una palabra reservada
      if token in defs.RESERVERD_WORDS:
        tokens_types.append({'type': defs.RESERVERD_WORDS[token], 'value': token})
      #! Identificamos si el token es una palabra reservada temporal
      elif token in defs.TEMP_RESERVED_WORDS:
        tokens_types.append({'type': defs.TEMP_RESERVED_WORDS[token], 'value': GL_LISTS[token][0]})
        GL_LISTS[token].pop(0)
      else:
        tokens_types.append({'type': 'TP_IDENTIFIER', 'value': token})
    #! Identificamos si el token es un numero
    elif defs.LITERA_INTEGER.match(token):
      tokens_types.append({'type': 'TP_INTEGER', 'value': token})
    #! Identificamos si el token es un operador
    elif token in defs.OPERATORS:
      tokens_types.append({'type': defs.OPERATORS[token], 'value': token})
    #! Identificamos si el token es un simbolo
    elif token in defs.SYMBOLS:
      tokens_types.append({'type': defs.SYMBOLS[token], 'value': token})

  logger.debug("Resulting tokens: " + str(tokens_types))

  print_break_line()
  return tokens_types, is_comment_block

def Get_tokens_list_from_file(file_name, debug_mode = False):
  logger.setLevel(logging.DEBUG) if debug_mode else logger.setLevel(logging.INFO)
  file_handler.setLevel(logging.DEBUG) if debug_mode else file_handler.setLevel(logging.INFO)

  file_type = file_name.split(".")[-1]
  if file_type == "quetzal":
    file = open(file_name, "r")

    logger.debug("Reading file: " + file_name)
    file_lines = file.readlines()
    print_break_line()

    tokens = []
    is_comment_block = False
    for line in file_lines:
      temp_tokens, is_comment_block = Get_tokens_list_from_line(line, is_comment_block)
      tokens.append(temp_tokens)
    definitions = [item for sublist in tokens for item in sublist]
    
    return definitions

  else:
    stream_handler.setFormatter(logging.Formatter('\033[91m'+'%(asctime)s:%(levelname)s: %(message)s'))
    logger.error("File type not supported. Only .quetzal files are supported")
    stream_handler.setFormatter(stream_formatter)
    return