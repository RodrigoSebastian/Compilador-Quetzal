import sys
from lexical_reader import Get_tokens_list_from_file

if __name__ == "__main__":
  print("Starting Quetzal compiler...")

  debug_mode = False
  if len(sys.argv) > 1:
    if sys.argv[1] == "debug":
      debug_mode = True

  Get_tokens_list_from_file("./code_examples/000_test.quetzal", debug_mode=debug_mode)