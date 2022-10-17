import re

RESERVERD_WORDS = {
  "and"   : "RW_AND"   , "false": "RW_FALSE", "or"  : "RW_OR"  , "break": "RW_BREAK", "if"  : "RW_IF"  ,
  "return": "RW_RETURN", "dec"  : "RW_DEC"  , "inc" : "RW_INC" , "true" : "RW_TRUE" , "elif": "RW_ELIF",
  "loop"  : "RW_LOOP"  , "var"  : "RW_VAR"  , "else": "RW_ELSE", "not"  : "RW_NOT"
}

OPERATORS = {
  '-' : 'OP_MINUS'        , '+' : 'OP_PLUS' , '*' : 'OP_MULTIPLY' , '/': 'OP_DIVIDE' , '%': 'OP_MODULO', 
  '=' : 'OP_ASSIGN'       , '==': 'OP_EQUAL', '!=': 'OP_NOT_EQUAL', '>': 'OP_GREATER', '<': 'OP_LESS'  , 
  '>=': 'OP_GREATER_EQUAL', '<=': 'OP_LESS_EQUAL'
}

TEMP_RESERVED_WORDS = {
  'TP_STRING': 'lit-str', 'TP_CHAR': 'lit-char'
}

IDENTIFIER = re.compile(r'[A-Za-z][A-Za-z0-9_]*')
LITERA_INTEGER = re.compile(r'-?[0-9]+')
LITERAL_CHAR = re.compile(r'\'[^\']*\'')
LITERAL_STRING = re.compile(r'"[^"]*"')
COMMENT = re.compile(r"//.*")
START_COMMENT_BLOCK = re.compile(r'/\*.*')
END_COMMENT_BLOCK = re.compile(r'.*\*/')
COMMENT_BLOCK = re.compile(r'/\*.*\*/')
