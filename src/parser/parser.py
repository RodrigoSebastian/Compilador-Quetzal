import pandas as pd
from src.custom_logger import CustomLogger

clogger = CustomLogger(file_name='parser.log', name='parser')

data = pd.read_csv('./src/parser/config/test.csv')
grammar = open('./src/parser/config/grammar_test.txt', 'r')
grammar = grammar.readlines()
estados = [["S'",'S']]
for row in grammar:
  row = row.split('->')
  estados.append([row[0].replace(' ',''),row[-1].strip()])

tokens_estados = {}

token_types = data.columns
for token_type in token_types:
  tokens_estados[token_type] = data[token_type].tolist()
