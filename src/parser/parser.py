from tabulate import tabulate
import pandas as pd
from src.custom_logger import CustomLogger
from src.error_manager import ErrorManager
from src.lexical.definitions import Definitions

clogger = CustomLogger(name='parser')
emanager = ErrorManager()
tokens_estados = {}
estados = []
defs = Definitions()

def init():
  global estados
  global tokens_estados

  data = pd.read_csv('./src/parser/config/LR_TABLE.csv')
  data = data.fillna('-')
  grammar = open('./src/parser/config/grammar.txt', 'r')
  grammar = grammar.readlines()
  estados = []
  for row in grammar:
    row = row.split('->')
    estados.append([row[0].replace(' ',''),row[-1].strip()])

  tokens_estados = {}

  token_types = data.columns
  for token_type in token_types:
    tokens_estados[token_type] = data[token_type].tolist()

  temp = []
  for token_type_int in defs.TOKEN_TYPES_INT:
    temp.append([token_type_int,defs.TOKEN_TYPES_INT[token_type_int]])
  clogger.debug("New token types int list:\n{0}".format(tabulate(temp, headers=['Token', 'INT'], showindex="always", tablefmt="pretty")))

def analyze_input(_input):
  init()
  input = []
  for token in _input:
    input.append(token['token'])
  stack = [0]

  input.append('EOF')

  log_temp = ""
  log_temp += "Stack: {0}\n".format(stack)
  log_temp += "\tInput: {0}".format(input)
  clogger.debug(log_temp)

  current_rule = 0
  error = False
  index = -1
  while current_rule != 'acc' and error == False:
    current_state = stack[-1]
    current_input = input[0]
    current_rule = tokens_estados[current_input][current_state]
    log_temp = ""
    log_temp += "Current state: {0}\n".format(current_state)
    log_temp += "\tCurrent rule: {0}\n".format(tokens_estados[current_input][current_state])
    
    if current_rule == '-':
      msg = emanager.get_syntax_error_message(_input[index]['token'])
      clogger.error(msg,'SYNTAX ERROR')
      return False
    else:
      if current_rule[0] == 's':
        stack.append(current_input)
        stack.append(int(current_rule[1:]))
        input.pop(0)
      elif current_rule[0] == 'r':
        reduc = estados[int(current_rule[1:])][1].split(' ')
        reduc.reverse()
        for reduc_item in reduc:
          if not stack == [0]:
            last_value_in_stack = stack[-2:]
            if last_value_in_stack[0] == reduc_item:
              stack.pop()
              stack.pop()

        new_stack_number = stack[-1]
        stack.append(estados[int(current_rule[1:])][0])
        new_stack_top = tokens_estados[stack[-1]][new_stack_number]

        stack.append(int(new_stack_top))
      log_temp += "\tInput: {0}\n".format(input)
      log_temp += "\tStack: {0}".format(stack)
      clogger.debug(log_temp)
      clogger.print_break_line()
      index += 1

  clogger.one_line().info("Parser: File is syntactically correct")
  return True