import logging
import os

from logger_config import LoggerConfig

class CustomLogger(object):
  logger = None
  file_handler = None
  stream_handler = None

  def __init__(self,file_name='my_app.log'):
    super().__init__()
    
    #! Crea la carpeta log_info si no existe
    os.mkdir('log_info') if not os.path.exists('log_info') else None

    #! Configura el logger para manejar errores y advertencias
    self.logger = logging.getLogger(__name__)
    self.logger.setLevel(logging.DEBUG)

    self.file_handler = logging.FileHandler(os.path.join('log_info',file_name))
    self.file_handler.setLevel(logging.INFO)
    self.file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: \n\t%(message)s'))

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
    return self

  def debug(self, msg):
    self.logger.debug(msg)
    self.stream_handler.setFormatter(LoggerConfig('%(asctime)s:%(levelname)s: ','\n\t%(message)s'))
  
  def info(self, msg):
    self.logger.info(msg)
    self.stream_handler.setFormatter(LoggerConfig('%(asctime)s:%(levelname)s: ','\n\t%(message)s'))
  
  def warning(self, msg):
    self.logger.warning(msg)
    self.stream_handler.setFormatter(LoggerConfig('%(asctime)s:%(levelname)s: ','\n\t%(message)s'))

  def error(self, msg):
    self.logger.error(msg)
    self.stream_handler.setFormatter(LoggerConfig('%(asctime)s:%(levelname)s: ','\n\t%(message)s'))

  def critical(self, msg):
    self.logger.critical(msg)
    self.stream_handler.setFormatter(LoggerConfig('%(asctime)s:%(levelname)s: ','\n\t%(message)s'))