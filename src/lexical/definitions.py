import re

RESERVERD_WORDS = {
  "and"   : "and"   , "or"  : "or"  , "break": "break", "if"   : "if"  ,
  "return": "return", "dec" : "dec" , "inc"  : "inc"  , "elif" : "elif",
  "loop"  : "loop"  , "var" : "var" , "else" : "else" , "not"  : "not"
}

OPERATORS = {
  '-': 'OP_MINUS' , '+': 'OP_PLUS'   , '*': 'OP_MULTIPLY' , '/': 'OP_DIVIDE' , '%': 'OP_MODULO', 
  '=': 'OP_ASSIGN', '>': 'OP_GREATER', '<': 'OP_LESS'
}

DB_OPERATORS = {
  '>=': 'OP_GREATER_EQUAL', '<=': 'OP_LESS_EQUAL', '==': 'OP_EQUAL', '!=': 'OP_NOT_EQUAL'
}

SYMBOLS = {
  '\n': 'SB_BREAK_LINE'   , ';' : 'SB_SEMI_COLON'      , ',': 'SB_COMMA'            , '.' : 'SB_DOT'          ,
  ':' : 'SB_COLON'        , '(' : 'SB_LEFT_PARENTHESIS', ')': 'SB_RIGHT_PARENTHESIS', '[' : 'SB_LEFT_BRACKET' ,
  ']' : 'SB_RIGHT_BRACKET', '{' : 'SB_LEFT_BRACE'      , '}': 'SB_RIGHT_BRACE'      , '|' : 'SB_PIPE'         ,
  '!' : 'SB_EXCLAMATION'  , '#' : 'SB_HASH'            , '@': 'SB_AT'               , '\t': 'SB_TAB'          ,
  '?' : 'SB_QUESTION_MARK'
}

TOKEN_TYPES = {
  'TP_INDENTIFIER': 'ID',
  'TP_INTEGER'    : 'LIIN',
  'TP_STRING'     : 'LISTR',
  'TP_CHAR'       : 'LICH',
  'TP_ES_CHAR'    : 'LICH',
  'TP_UC_CHAR'    : 'LICH',
  'false'         : 'LIBO',
  'true'          : 'LIBO',
}

TOKEN_TYPES_INT = {
  'Q'       : -5,
  'EOF'     : -1,
  'PROGRAMP':  1,
  'PROGRAM' :  2,
  'ID'      :  3,
  'LIIN'    :  4,
  'LISTR'   :  5,
  'LICH'    :  6,
  'LIBO'    :  7
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