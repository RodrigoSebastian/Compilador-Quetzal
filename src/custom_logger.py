import logging
import os
from src.logger_config import LoggerConfig

class CustomLogger(object):
  logger = None
  file_handler = None
  stream_handler = None

  file_format = logging.Formatter('%(asctime)s:%(levelname)s: \n\t%(message)s')

  def __init__(self,file_name='my_app.log'):
    super().__init__()
    
    #! Crea la carpeta log_info si no existe
    os.mkdir('log_info') if not os.path.exists('log_info') else None

    #! Configura el logger para manejar errores y advertencias
    self.logger = logging.getLogger(__name__)
    self.logger.setLevel(logging.DEBUG)

    self.file_handler = logging.FileHandler(os.path.join('log_info',file_name))
    self.file_handler.setLevel(logging.INFO)
    self.file_handler.setFormatter(self.file_format)

    self.stream_handler = logging.StreamHandler()
    self.stream_handler.setFormatter(LoggerConfig())

    self.logger.addHandler(self.file_handler)
    self.logger.addHandler(self.stream_handler)

  def __new__(cls, *args, **kwargs):
    if not hasattr(cls, 'instance'):
      cls.instance = super(CustomLogger, cls).__new__(cls)
    return cls.instance

  def one_line(self):
    self.stream_handler.setFormatter(LoggerConfig('%(asctime)s:%(levelname)s: ','%(message)s'))
    self.file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
    return self

  def without_format(self):
    self.stream_handler.setFormatter(LoggerConfig('','%(message)s'))
    self.file_handler.setFormatter(logging.Formatter('%(message)s'))
    return self

  def setLevel(self, level = 'DEBUG'):
    if level == 'DEBUG':
      self.logger.setLevel(logging.DEBUG)
      self.file_handler.setLevel(logging.DEBUG)
    elif level == 'INFO':
      self.logger.setLevel(logging.INFO)
      self.file_handler.setLevel(logging.INFO)
    elif level == 'WARNING':
      self.logger.setLevel(logging.WARNING)
      self.file_handler.setLevel(logging.WARNING)
    elif level == 'ERROR':
      self.logger.setLevel(logging.ERROR)
      self.file_handler.setLevel(logging.ERROR)
    elif level == 'CRITICAL':
      self.logger.setLevel(logging.CRITICAL)
      self.file_handler.setLevel(logging.CRITICAL)
    else:
      self.logger.setLevel(logging.NOTSET)
      self.file_handler.setLevel(logging.INFO)

  def debug(self, msg):
    self.logger.debug(msg)
    self.stream_handler.setFormatter(LoggerConfig('%(asctime)s:%(levelname)s: ','\n\t%(message)s'))
    self.file_handler.setFormatter(self.file_format)
  
  def info(self, msg):
    self.logger.info(msg)
    self.stream_handler.setFormatter(LoggerConfig('%(asctime)s:%(levelname)s: ','\n\t%(message)s'))
    self.file_handler.setFormatter(self.file_format)
  
  def warning(self, msg):
    self.logger.warning(msg)
    self.stream_handler.setFormatter(LoggerConfig('%(asctime)s:%(levelname)s: ','\n\t%(message)s'))
    self.file_handler.setFormatter(self.file_format)

  def error(self, msg):
    self.logger.error(msg)
    self.stream_handler.setFormatter(LoggerConfig('%(asctime)s:%(levelname)s: ','\n\t%(message)s'))
    self.file_handler.setFormatter(self.file_format)

  def critical(self, msg):
    self.logger.critical(msg)
    self.stream_handler.setFormatter(LoggerConfig('%(asctime)s:%(levelname)s: ','\n\t%(message)s'))
    self.file_handler.setFormatter(self.file_format)