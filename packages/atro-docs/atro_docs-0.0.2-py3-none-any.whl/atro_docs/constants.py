import logging
from pathlib import Path
import tempfile

REPOS_YAML_FILE_NAME = ".doc.repos.yaml"
TEMP_DOCS_DIR = Path(tempfile.mkdtemp())
MKDOCS_INFO_LINE_START="INFO    -  "
MKDOCS_WARNING_LINE_START="\x1b[33mWARNING -  \x1b[0m"


def _get_constants():
    # Get all attributes of the current module (which is __main__ when inside the module)
    current_module = globals()
    # Filter only for constants (assuming they're all uppercase)
    return {name: value for name, value in current_module.items() if name.isupper()}

logging.info("Loaded constants.py with constants: " +  str(_get_constants()))
