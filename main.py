from tabulate import tabulate
import sys
from lexical_reader import Get_tokens_list_from_file

#! Funcion para la tabla de simbolos
def print_tokens(definitions):
  only_for_print = []
  for definition in definitions:
    temp = []
    temp.append(definition['type'])
    temp.append(definition['value'])
    only_for_print.append(temp)
  
  print(tabulate(only_for_print, headers=['Tipo', 'Valor']))
  
if __name__ == "__main__":
  print("Starting Quetzal compiler...")

  debug_mode = False
  if len(sys.argv) > 1:
    if sys.argv[1] == "debug":
      debug_mode = True

  definitions = Get_tokens_list_from_file("./code_examples/000_test.quetzal", debug_mode=debug_mode)
  # definitions = Get_tokens_list_from_file("./code_examples/001_hello.quetzal", debug_mode=debug_mode)
  # definitions = Get_tokens_list_from_file("./code_examples/002_binary.quetzal", debug_mode=debug_mode)
  print_tokens(definitions)