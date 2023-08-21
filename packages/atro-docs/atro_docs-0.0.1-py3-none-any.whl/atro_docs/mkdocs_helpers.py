from enum import Enum
from sh import mkdocs, killall # type: ignore
from pathlib import Path
import logging 
from constants import MKDOCS_INFO_LINE_START, MKDOCS_WARNING_LINE_START

class LineStartTypes(Enum):
   Info = "Info"
   Warning = "Warning"

latest_line_start = None
combined_text = ""

def process_output(line):
    global latest_line_start
    global combined_text

    line = str(line)

    if line.startswith(MKDOCS_INFO_LINE_START):
      print_combined_text()
      latest_line_start = LineStartTypes.Info
      
    elif line.startswith(MKDOCS_WARNING_LINE_START):
      print_combined_text()
      latest_line_start = LineStartTypes.Warning
    
    
    
    combined_text += line

def print_combined_text():
    global combined_text
    global latest_line_start

    match (latest_line_start):
      case LineStartTypes.Info:
        combined_text = combined_text.strip(MKDOCS_INFO_LINE_START)
      case LineStartTypes.Warning:
        combined_text = combined_text.strip(MKDOCS_WARNING_LINE_START)
      case _:
          pass

    # trim time if its present
    if len(combined_text) > 10 and combined_text[0] == "[" and combined_text[9] == "]":
       combined_text = combined_text[11:]
       
    match (latest_line_start):
      case LineStartTypes.Info:
        logging.info(combined_text)
      case LineStartTypes.Warning:
        logging.warning(combined_text)
      case _:
          pass
    combined_text = ""


def run_mkdocs(docs_parent_dir: Path, bg: bool = False):
  # Kill all mkdocs instances if any
  try:
    killall("mkdocs")
  except:
    pass
  
  output = mkdocs("serve", "--dev-addr=0.0.0.0:8093", _cwd=docs_parent_dir.as_posix(), _out=process_output, _err=process_output, _bg=bg)
  output.wait()

