from src.custom_logger import CustomLogger
import re

class Definitions(object):
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

  GL_LISTS = {}
  GL_COMPILERS = {}
  GL_SYMBOL_TABLE = []
  GL_ENVIRONMENT = []

  clogger = CustomLogger(name='definitions')

  def __new__(cls, *args, **kwargs):
    if not hasattr(cls, 'instance'):
      cls.instance = super(Definitions, cls).__new__(cls)
    return cls.instance

  def __getattribute__(self, __name):
    return super(Definitions, self).__getattribute__(__name)

  #! Funcion para inicializar las variables globales
  def custom_init(self):
    for db_operator in self.DB_OPERATORS:
      if db_operator not in self.GL_COMPILERS:
        self.GL_COMPILERS[db_operator] = re.compile(r'{0}'.format(db_operator))
      if 'TP_{0}'.format(self.DB_OPERATORS[db_operator]) not in self.TEMP_RESERVED_WORDS:
        self.TEMP_RESERVED_WORDS['TP_{0}'.format(self.DB_OPERATORS[db_operator])] = self.DB_OPERATORS[db_operator]

    amount_tokens = len(self.TOKEN_TYPES_INT)
    for element in self.SYMBOLS:
      self.TOKEN_TYPES[self.SYMBOLS[element]] = element
      self.TOKEN_TYPES_INT[element] = amount_tokens
      amount_tokens += 1

    amount_tokens = len(self.TOKEN_TYPES_INT)
    for element in self.RESERVERD_WORDS:
      self.TOKEN_TYPES_INT[self.RESERVERD_WORDS[element]] = amount_tokens
      amount_tokens += 1

    amount_tokens = len(self.TOKEN_TYPES_INT)
    for element in self.OPERATORS:
      self.TOKEN_TYPES[self.OPERATORS[element]] = element
      self.TOKEN_TYPES_INT[element] = amount_tokens
      amount_tokens += 1

    amount_tokens = len(self.TOKEN_TYPES_INT)
    for element in self.DB_OPERATORS:
      self.TOKEN_TYPES[self.DB_OPERATORS[element]] = element
      self.TOKEN_TYPES_INT[element] = amount_tokens
      amount_tokens += 1