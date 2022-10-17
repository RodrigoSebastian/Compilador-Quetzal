import sys
from lexical_reader import Get_tokens_list_from_file
  
if __name__ == "__main__":
  debug_mode = False
  if len(sys.argv) > 1:
    if sys.argv[1] == "debug":
      debug_mode = True

  definitions = Get_tokens_list_from_file("./code_examples/000_test.quetzal", debug_mode=debug_mode)
  # definitions = Get_tokens_list_from_file("./code_examples/001_hello.quetzal", debug_mode=debug_mode)
  # definitions = Get_tokens_list_from_file("./code_examples/002_binary.quetzal", debug_mode=debug_mode)
  # print_tokens(definitions)