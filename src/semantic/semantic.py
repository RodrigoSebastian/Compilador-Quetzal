from src.lexical.definitions import Definitions
from src.error_manager import ErrorManager
from src.custom_logger import CustomLogger

clogger = CustomLogger(name='semantic')
emanager = ErrorManager()
defs = Definitions()

def validate_semantic(definitions, original_file):

  file = open(original_file, 'r')
  lines = file.readlines()
  lines = [line.replace('\n','') for line in lines]

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
  for idx1, variable in enumerate(defs.GL_SYMBOL_TABLE):
    for idx2, variable2 in enumerate(defs.GL_SYMBOL_TABLE):
      if variable['token'] == variable2['token'] and variable['environment'] == variable2['environment'] and idx1 != idx2:
        print(variable)
        msg = emanager.get_semanctic_error_message('It\'s an error to define two global variables with the same name.\nYou have another variable is in line {0}.'.format(variable2['line']), variable['token'], variable['line'])
        clogger.error(msg,'SEMANTIC ERROR')
        return False

  # 6. It’s an error to define two functions with the same name.
  for idx1, function in enumerate(defs.GL_FUNCTION_DEFINITIONS):
    for idx2, function2 in enumerate(defs.GL_FUNCTION_DEFINITIONS):
      if function['name'] == function2['name'] and idx1 != idx2:
        msg = emanager.get_semanctic_error_message('It\'s an error to define two functions with the same name.\nYou have another function is in line {0}.'.format(function['line']), function['name'], function2['line'])
        clogger.error(msg,'SEMANTIC ERROR')
        return False

  # 7. A function definition is visible from the body of all the functions in a program, even from itself.
  # Thus, functions can call themselves recursively directly or indirectly.
  for function in defs.GL_FUNCTION_DEFINITIONS:
    for variable in defs.GL_SYMBOL_TABLE:
      if variable['token'] == function['name']:
        if int(variable['environment']) != 0:
          msg = emanager.get_semanctic_error_message('A function definition is visible from the body of all the functions in a program, even from itself.', function['name'], function['line'])
          clogger.error(msg,'SEMANTIC ERROR')
          return False

  # 8. In every function call the number of arguments must match the number of
  # parameters contained in the corresponding function definition.
  for function in defs.GL_FUNCTION_DEFINITIONS:
    for variable in defs.GL_SYMBOL_TABLE:
      if variable['token'] == function['name'][:-2] and len(variable['references']) > 0:
        for reference in variable['references']:
          linea_referencia = lines[reference-1]
          tempo_index = linea_referencia.find(variable['token'])
          temp2 = tempo_index
          params_stack = 0
          param_count = 0
          funcion = ""
          for ff in range(tempo_index,len(linea_referencia)):
            funcion = funcion + linea_referencia[ff]
            if linea_referencia[ff] == '(': params_stack += 1
            if linea_referencia[ff] == ')': params_stack -= 1
            if params_stack <= 0 and linea_referencia[ff] not in variable['token']:
              break
          start_parameters = funcion.find('(') + 1
          parameters = funcion[start_parameters:-1]
          have_function = parameters.find('(')
          end_function = parameters.find(')')
          res = list(range(have_function,end_function + 1))
          while have_function != -1:
            parameters = ''.join([param for idx, param in enumerate(parameters) if idx not in res])

            have_function = parameters.find('(')
            end_function = parameters.find(')')
            res = list(range(have_function,end_function + 1))

          param_count = len([value for value in parameters.split(',') if value != ''])

          if param_count != function['parameters']:
            msg = emanager.get_semanctic_error_message('In every function call the number of arguments must match the number of parameters contained in the corresponding function definition.\nThe function {0} has {1} parameters and you are passing {2}.'.format(function['name'], function['parameters'], param_count), variable['token'], reference)
            clogger.error(msg,'SEMANTIC ERROR')
            return False

  # 10. Each function has its own independent namespace for its local names.
  # This means that parameter and local variable names have to be unique inside the body of each function.
  # It’s valid to have a parameter or local variable name with the same name as a global variable.
  # In that case the local name shadows the global variable.

  # 11. It’s an error to refer to a variable, parameter or function not in scope in the current namespace. -> OK

  # 12. The break statement can only be used inside the body of a loop statement. TODO
  final_break = []
  for loop in defs.GL_LOOP_SCOPE:
    for breack in defs.GL_BREAK_SCOPE:
      if len(breack['path'].replace(loop['path'],'')) == 0:
        final_break.append(breack)

  if len(final_break) > 0:
    msg = emanager.get_semanctic_error_message('The break statement can only be used inside the body of a loop statement.', 'break', defs.GL_BREAK_SCOPE[0]['line'] + 1)
    clogger.error(msg,'SEMANTIC ERROR')
    return False

  # 13. Values of integer literals should be between -2147483648 and 2147483647 (−231 and 231−1, respectively).
  for definition in definitions:
    if definition['token'] == 'LIIN':
      if int(definition['extra_info']) < -2147483648 or int(definition['extra_info']) > 2147483647:
        msg = emanager.get_semanctic_error_message('Values of integer literals should be between -2147483648 and 2147483647 (−231 and 231−1, respectively).', definition['value'], definition['line'] + 1)
        clogger.error(msg,'SEMANTIC ERROR')
        return False


  clogger.one_line().info("Semantic: File is semantically correct")
  return True