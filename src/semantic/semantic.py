from src.lexical.definitions import Definitions
from src.error_manager import ErrorManager
from src.custom_logger import CustomLogger

clogger = CustomLogger(name='semantic')
emanager = ErrorManager()
defs = Definitions()

def validate_semantic(definitions):

  # defs.GL_SYMBOL_TABLE[15]['type'] = 'Int'
  # 1. The language only supports a 32-bit signed two’s complement integer (int32) data type. 
  # This is the data type for every variable, parameter and function return value. 
  # This means that a Quetzal Dragon compiler doesn’t need to verify type consistency.
  for variable in defs.GL_SYMBOL_TABLE:
    if variable['type'] != 'Int32':
      msg = emanager.get_semanctic_error_message('The language only supports a 32-bit signed two\'s complement integer (Int32) data type.', variable['token'], variable['line'])
      clogger.error(msg,'SEMANTIC ERROR')
      return False

  # 2. Every program starts its execution in a function called main.
  # It is an error if the program does not contain a function with this name. 
  # It is also an error if the main function defines one or more parameters.
  # del defs.GL_FUNCTION_DEFINITIONS['main()']
  # defs.GL_FUNCTION_DEFINITIONS['main()'] = 4
  have_main = False
  for function in defs.GL_FUNCTION_DEFINITIONS:
    if function['name'] == 'main()':
      have_main = True
      if function['parameters'] != 0:
        msg = emanager.get_semanctic_error_message('The main function defines one or more parameters.', None, 0)
        clogger.error(msg,'SEMANTIC ERROR')
        return False

  if not have_main:
    msg = emanager.get_semanctic_error_message('Every program starts its execution in a function called main.', None, 0)
    clogger.error(msg,'SEMANTIC ERROR')
    return False

  # 3. Any variable defined outside a function is a global variable.
  # The scope of a global variable is the body of all the functions in the program,
  # even those defined before the variable itself.

  # 4. Function names and global variables exist in different namespaces.
  # This means that you can have a global variable with the same name as a function and vice versa.   -> OK

  # 5. It’s an error to define two global variables with the same name.

  # 6. It’s an error to define two functions with the same name.

  # 7. A function definition is visible from the body of all the functions in a program, even from itself.
  # Thus, functions can call themselves recursively directly or indirectly.

  # 8. In every function call the number of arguments must match the number of
  # parameters contained in the corresponding function definition.

  # 10. Each function has its own independent namespace for its local names.
  # This means that parameter and local variable names have to be unique inside the body of each function.
  # It’s valid to have a parameter or local variable name with the same name as a global variable.
  # In that case the local name shadows the global variable.

  # 11. It’s an error to refer to a variable, parameter or function not in scope in the current namespace. -> OK

  # 12. The break statement can only be used inside the body of a loop statement.

  # 13. Values of integer literals should be between -2147483648 and 2147483647 (−231 and 231−1, respectively).


  clogger.one_line().info("Semantic: File is semantically correct")
  return True