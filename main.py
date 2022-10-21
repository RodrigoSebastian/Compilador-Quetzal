import sys
import os
import click
from lexical_reader import Get_tokens_list_from_file

@click.command()
@click.option('--file', '-f', help='The path to the file to be compiled [required if test mode is not enabled]', type=click.Path(exists=True), required=False)
@click.option('--debug', '-d', help='Enable debug mode to show detailed information about the process', is_flag=True)
@click.option('--test', '-t', help='Run the compiler with all the test files in this folder', type=click.Path(exists=True), required=False)
def veg(file, debug, test):
  debug_mode = debug
  if file:
    Get_tokens_list_from_file(file,debug_mode)
  elif test:
    if os.path.isdir(test):
      if test[-1] != "/":
        test += "/"
      files = os.listdir(test)
      files.sort()
      initial_path = test
      for file in files:
        path = initial_path + file
        if os.path.isdir(path): 
          temp_files = os.listdir(path)
          for temp_file in temp_files:
            temp_path = path + "/" + temp_file
            Get_tokens_list_from_file(temp_path,debug_mode,test_mode=test)
        else:
          Get_tokens_list_from_file(path,debug_mode,test_mode=test)  
    else:
      click.echo("The path is not a directory")
  else:
    click.echo('Please provide a file to read')

if __name__ == "__main__":
  veg()