import pandas as pd

data = pd.read_csv('./src/parser/config/test.csv')
grammar = open('./src/parser/config/grammar_test.txt', 'r')
grammar = grammar.readlines()
estados = [["S'",'S']]
for row in grammar:
  row = row.split('->')
  estados.append([row[0].replace(' ',''),row[-1].strip()])

tokens_estados = {}
# estados = data['Q'].tolist()

token_types = data.columns
for token_type in token_types:
  tokens_estados[token_type] = data[token_type].tolist()

for token in tokens_estados:
  print(token)
  print(tokens_estados[token])
  print("")

for estado in estados:
  print(estado)

def analyze_input(_input):
  print("Input: " + _input)
  _input = _input + '$'
  stack = [0]
  split_input = list(_input)
  print("Stack: " + str(stack))
  print("Split input: " + str(split_input))
  print("")

  while stack != [0,'S',1]:
  # for x in range(len(split_input)):
    print("Stack: " + str(stack))
    print("Input: " + str(split_input))

    current_state = stack[-1]
    current_input = split_input[0]
    current_rule = tokens_estados[current_input][current_state]
    print("Current rule: " + str(current_rule))
    if current_rule[0] == 's':
      stack.append(current_input)
      stack.append(int(current_rule[-1]))
      split_input.pop(0)
    elif current_rule[0] == 'r':
      reduc = list(estados[int(current_rule[-1])][1])
      reduc = reversed(reduc)
      for reduc_item in reduc:
        if type(stack[-1]) == int:
          stack.pop()
        if stack[-1] == reduc_item:
          stack.pop()

      new_stack_number = stack[-1]
      stack.append(estados[int(current_rule[-1])][0])
      new_stack_top = tokens_estados[stack[-1]][new_stack_number]

      stack.append(int(new_stack_top))

    print("")

  print("Cadena aceptada")
    

# cadena = 'abbcde'
cadena = 'abbcbcbcde'
analyze_input(cadena)

# print("Data: ", data)
# print("Data: ", data.columns)
# print("Data: ", data.index)
# print("Data Values: ", data.values)
# for i in data.values:
#     print(i)
# print("Data: ", data.shape)
# print("Data: ", data.size)
# print("Data: ", data.ndim)
# print("Data: ", data.dtypes)
# print("Data: ", data.empty)