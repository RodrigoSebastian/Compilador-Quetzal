from distutils.dir_util import copy_tree
from hashlib import new
from re import T
from webbrowser import get
from src.custom_logger import CustomLogger
from src.error_manager import ErrorManager
from src.lexical.definitions import Definitions

from treelib import Node, Tree
from tabulate import tabulate
import pandas as pd

clogger = CustomLogger(name='parser')
emanager = ErrorManager()
tokens_estados = {}
estados = []
defs = Definitions()

tree_info = []

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
        tree_info.append(current_rule)
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
  
  print("\n=======================================\n")
  final_tree = recorrer(tree_info)
  print("\n=======================================\n")
  recorrer_final(final_tree,0)
  print("\n=======================================\n")
  return True

def testo(_tree_info):
  print(_tree_info)
  print("\n=======================================\n")
  final_tree = []

  for idx in range(2):
    state = estados[int(_tree_info[0][1:])]
    rule = state[0]
    deriv = state[1].split(' ')

    temp_info = [rule, deriv]
    
    if final_tree == []:
      final_tree = temp_info
    else:
      if rule in final_tree[1]:
        final_tree[1] = temp_info

    print("State: {0}".format(state))
    print("Rule: {0}".format(rule))
    print("Deriv: {0}".format(deriv))
    print("Temp info: {0}".format(temp_info))
    print("\n=======================================\n")
    _tree_info.pop(0)


  print("Final tree: {0}".format(final_tree))
  print("\n=======================================\n")

def recorrer_final(lista,tab):
  for l in lista:
    if type(l) == list:
      recorrer_final(l,tab+1)
    else:
      print(' ' * tab + l)

def recorrer(_tree_info):
  info_temporal = []
  index_info_temp = []
  stop = ''

  while stop != 'PROGRAM':
    original_state = estados[int(_tree_info[0][1:])]
    original_rule = original_state[0]
    original_deriv = original_state[1].split(' ')
    original_info = [original_rule, original_deriv]

    print('Tree info: {0}'.format(_tree_info[0]))
    print("State: {0}".format(original_state))
    print("Rule: {0}".format(original_rule))
    print("Deriv: {0}".format(original_deriv))

    new_deriv = []
    if original_deriv == ["''"]:
      if len(original_info[1]) == 1:
        original_info[1] = original_info[1][0]
      info_temporal.append(original_info)
      index_info_temp.append(original_rule)
    else:
      for item in original_deriv:
        if item in index_info_temp:
          index = index_info_temp.index(item)
          new_deriv.append(info_temporal[index])

          del info_temporal[index]
          del index_info_temp[index]
        else:
          new_deriv.append(item)

      if len(new_deriv) == 1:
        new_deriv = new_deriv[0]
      original_info = [original_rule, new_deriv]
      info_temporal.append(original_info)
      index_info_temp.append(original_rule)

    try:
      stop = info_temporal[0][0]
    except:
      stop = ''

    print("\n=======================================\n")
    _tree_info.pop(0)

  print("Temp info: {0}".format(info_temporal[0]))

  return info_temporal[0]