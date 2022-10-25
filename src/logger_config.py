import logging

class LoggerConfig(logging.Formatter):
  #! Colores para la consola
  red      = '\033[91m'
  blue     = '\033[38;5;39m'
  green    = '\033[92m'
  reset    = '\033[0m'
  yellow   = '\033[38;5;226m'
  bold_red = '\033[31;1m'

  format_prefix = '%(asctime)s:%(levelname)s: '
  format_suffix = '\n\t%(message)s'

  def __init__(self, fmt_prefix=format_prefix, fmt_suffix=format_suffix):
    super().__init__()
    error_format_suffix = '%(message)s'
    self.FORMATS = {
      logging.DEBUG: self.green + fmt_prefix + self.reset + fmt_suffix,
      logging.INFO: self.blue + fmt_prefix + self.reset + fmt_suffix,
      logging.WARNING: self.yellow + fmt_prefix + self.reset + fmt_suffix,
      logging.ERROR: self.red + fmt_prefix + error_format_suffix + self.reset,
      logging.CRITICAL: self.bold_red + fmt_prefix + error_format_suffix + self.reset
    }

  def change_prefix(self, prefix):
    self.format_prefix = prefix

  def change_suffix(self, suffix):
    self.format_suffix = suffix

  def change_format(self, prefix, suffix):
    self.change_prefix(prefix)
    self.change_suffix(suffix)
    self.__init__(prefix, suffix)

  def restart_format(self):
    self.__init__()

  def format(self, record):
    log_fmt = self.FORMATS.get(record.levelno)
    formatter = logging.Formatter(log_fmt)
    return formatter.format(record)