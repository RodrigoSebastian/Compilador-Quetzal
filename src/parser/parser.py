import pandas as pd
from src.custom_logger import CustomLogger
import src.lexical.definitions as defs

clogger = CustomLogger(name='parser')
tokens_estados = {}
estados = []

def init():
  global estados
  global tokens_estados

  data = pd.read_csv('./src/parser/config/LR_TABLE.csv')
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

def analyze_input(_input):
  init()
  input = []
  for token in _input:
    input.append(token['token'])
  stack = [0]

  input.append('EOF')

  print("Stack: {0}".format(stack))
  print("Input: {0}".format(input))
  print("")

  current_rule = 0
  while current_rule != 'acc':
  # for x in range(10):
    current_state = stack[-1]
    current_input = input[0]
    current_rule = tokens_estados[current_input][current_state]
    print("Current state: {0}".format(current_state))
    print("Current rule: {0}".format(tokens_estados[current_input][current_state]))
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

    print("Input: " + str(input))
    print("Stack: " + str(stack))
    print("")

  print("Cadena aceptada")