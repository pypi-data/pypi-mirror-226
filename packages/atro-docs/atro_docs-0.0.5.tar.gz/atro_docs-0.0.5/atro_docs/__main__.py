from atro_pylog import set_logger
from inputs import get_application
import logging

if __name__ == "__main__":
  application = get_application()
  
  # Fuck cleo logging bs.
  for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
  set_logger()
  
  application.run()