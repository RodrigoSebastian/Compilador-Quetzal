from ast import Return
import definitions as defs
import logging
import os

#! Create log_info folder if it doesn't exist
os.mkdir('log_info') if not os.path.exists('log_info') else None

#! Configure logger to manage errors and warnings
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:\n\t%(message)s')

file_handler = logging.FileHandler('log_info/lexical_reader.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

GL_LISTS = {}

def print_break_line():
  stream_handler.setFormatter(logging.Formatter('%(message)s'))
  file_handler.setFormatter(logging.Formatter('%(message)s'))
  logger.debug("=====================================================================")
  stream_handler.setFormatter(formatter)
  file_handler.setFormatter(formatter)

def replace_token_by_tory(_type_token, _line, _name = ""):
  line = _line
  token_list = _type_token.findall(line)
  for token in token_list:
    line = line.replace(token, _name)
    if _name != "":
      if _name.strip() not in GL_LISTS:
        GL_LISTS[_name.strip()] = []
      GL_LISTS[_name.strip()].append(token)

  logger.debug("Changing to {0}: {1}".format(_name.strip() if _name != "" else "BLANK if is a COMMENT",line)) if token_list else None
  return line

def Get_tokens_list_from_line(line, _is_comment_block = False):
  is_comment_block = _is_comment_block
  tokens = []

  if line == '\n':                                     #! Si la linea esta vacia, no hacer nada
    return [], is_comment_block

  if(len(defs.END_COMMENT_BLOCK.findall(line)) > 0):   #! Verifica si la linea es un fin de bloque de comentario
    is_comment_block = False

  if is_comment_block:                                 #! Si es un bloque de comentario, no se hace nada
    return [], is_comment_block

  logger.debug("Reading line: " + line.strip('\n'))

  #! Reemplazamos los strings por un token
  line = replace_token_by_tory(defs.LITERAL_STRING, line, ' TP_STRING ')
  #! Reemplazamos los caracteres por un token
  line = replace_token_by_tory(defs.LITERAL_CHAR, line, ' TP_CHAR ')
  
  #! Quitamos todos los comentarios existentes en la linea
  line = replace_token_by_tory(defs.COMMENT, line) 
  if(len(defs.START_COMMENT_BLOCK.findall(line)) > 0): #! Si la linea tiene un inicio de bloque de comentarios entonces
    is_comment_block = True                            #! se activa el modo de bloque de comentarios ignorando todas las
                                                       #! demás lineas hasta que se encuentre un fin de bloque de comentarios
  line = replace_token_by_tory(defs.START_COMMENT_BLOCK, line)
  line = replace_token_by_tory(defs.END_COMMENT_BLOCK, line)
  line = replace_token_by_tory(defs.COMMENT_BLOCK, line)

  logger.debug("Line after replacing words: " + line.strip('\n'))

  print_break_line()

  return tokens, is_comment_block

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

  else:
    logger.error("File type not supported. Only .quetzal files are supported")
    return