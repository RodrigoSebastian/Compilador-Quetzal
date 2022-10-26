import re

RESERVERD_WORDS = {
  "and"   : "RW_AND"   , "false": "RW_FALSE", "or"  : "RW_OR"  , "break": "RW_BREAK", "if"  : "RW_IF"  ,
  "return": "RW_RETURN", "dec"  : "RW_DEC"  , "inc" : "RW_INC" , "true" : "RW_TRUE" , "elif": "RW_ELIF",
  "loop"  : "RW_LOOP"  , "var"  : "RW_VAR"  , "else": "RW_ELSE", "not"  : "RW_NOT"
}

OPERATORS = {
  '-': 'OP_MINUS' , '+': 'OP_PLUS'   , '*': 'OP_MULTIPLY' , '/': 'OP_DIVIDE' , '%': 'OP_MODULO', 
  '=': 'OP_ASSIGN', '>': 'OP_GREATER', '<': 'OP_LESS'
}

DB_OPERATORS = {
  '>=': 'OP_GREATER_EQUAL', '<=': 'OP_LESS_EQUAL', '==': 'OP_EQUAL', '!=': 'OP_NOT_EQUAL'
}

SYMBOLS = {
  '\n': 'SB_BREAK_LINE'   , ';' : 'SB_SEMI_COLON'      , ',': 'SB_COMMA'            , '.': 'SB_DOT'          ,
  ':' : 'SB_COLON'        , '(' : 'SB_LEFT_PARENTHESIS', ')': 'SB_RIGHT_PARENTHESIS', '[': 'SB_LEFT_BRACKET' ,
  ']' : 'SB_RIGHT_BRACKET', '{' : 'SB_LEFT_BRACE'      , '}': 'SB_RIGHT_BRACE'      , '|': 'SB_PIPE'         ,
  '!' : 'SB_EXCLAMATION'  , '#' : 'SB_HASH'            , '@': 'SB_AT'               , '$': 'SB_DOLLAR'       ,
  '\t': 'SB_TAB'
}

TEMP_RESERVED_WORDS = {
  'TP_STRING': 'TP_STRING', 'TP_CHAR': 'TP_CHAR', 'TP_ES_CHAR': 'TP_ES_CHAR', 'TP_UC_CHAR': 'TP_UC_CHAR'
}

IDENTIFIER = re.compile(r'[A-Za-z][A-Za-z0-9_]*')
LITERA_INTEGER = re.compile(r'-?[0-9]+')
LITERAL_CHAR = re.compile(r'\'[^\']\'')
LITERAL_ESCAPED_CHAR = re.compile(r'(\'\\[tnr\\\'"]\')')
LITERAL_UNICODE_CHAR = re.compile(r'\'\\u[0-9a-fA-F]{6}\'')
LITERAL_STRING = re.compile(r'"(?:[^\\"]|\\.)*"')
COMMENT = re.compile(r"//.*")
START_COMMENT_BLOCK = re.compile(r'/\*.*')
END_COMMENT_BLOCK = re.compile(r'.*\*/')
COMMENT_BLOCK = re.compile(r'/\*.*\*/')
