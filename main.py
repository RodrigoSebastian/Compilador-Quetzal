import sys
import os

from lexical_reader import Get_tokens_list_from_file
  
if __name__ == "__main__":
  debug_mode = False
  if len(sys.argv) > 1:
    if sys.argv[1] == "debug":
      debug_mode = True

  files = os.listdir('./code_examples')
  for file in files:
    definitions = Get_tokens_list_from_file('./code_examples/{0}'.format(file), debug_mode)
    print(" ")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print(" ")

  # definitions = Get_tokens_list_from_file("./code_examples/000_test.quetzal", debug_mode=debug_mode)