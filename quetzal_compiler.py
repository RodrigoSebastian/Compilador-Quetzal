import os
import click
from src.lexical.lexical_reader import Get_tokens_list_from_file
import src.parser.parser as ps
from src.custom_logger import CustomLogger

CURRENT_VERSION = '2.2.2'
clogger = CustomLogger(name='main')

@click.command()
@click.option('--file', '-f', help='The path to the file to be compiled [required if test mode is not enabled]', type=click.Path(exists=True))
@click.option('--test', '-t', help='Run the compiler with all the test files in this folder [required if file mode is not enabled]', type=click.Path(exists=True))
@click.option('--debug', '-d', help='Enable debug mode to show detailed information about the process', is_flag=True)
@click.option('--version', '-v', help='Show the current version of the compiler', is_flag=True)
def veg(file, debug, test, version):
  debug_mode = debug
  if version:
    click.echo("Quetzal compiler version {0}".format(CURRENT_VERSION))
  elif file:
    compile(file,debug_mode)
  elif test:
    if os.path.isdir(test):
      if test[-1] != '/':
        test += '/'

      files = os.listdir(test)
      files.sort()
      initial_path = test
      read_files(initial_path,files,debug_mode,test)
    else:
      click.echo("The path is not a directory")
  else:
    click.echo('Please provide a file to read with a --file or --test option')
    click.echo('Use --help for more information')

def read_files(initial_path,_files,debug_mode,test):
  for file in _files:
    path = initial_path + file
    if os.path.isdir(path):
      temp_files = os.listdir(path)
      read_files(path + '/',temp_files,debug_mode,test)
    else:
      compile(path,debug_mode,test)
      clogger.without_format().info("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

def compile(path,debug_mode,test = False):
  definitions = Get_tokens_list_from_file(path,debug_mode,test)
  if definitions != []:  
    definitions = ps.analyze_input(definitions)
    if definitions:
      clogger.one_line().info("The code has been compiled successfully")
      clogger.without_format().info("")

if __name__ == "__main__":
  veg()