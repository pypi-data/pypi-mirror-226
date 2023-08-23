from cleo.commands.command import Command
from cleo.helpers import argument, option 
from cleo.application import Application
from atro_docs import repo
from temp_dir import prepare_temp_dir
from pathlib import Path
from constants import TEMP_DOCS_DIR
from mkdocs_helpers import run_mkdocs
from webhook import run_webhook_server

class RunMkDocsCommand(Command):
    name = "run"
    description: str = "Runs mkdocs serve"
    arguments = [
        argument(
            "repo",
            description="Which repo to run? By default runs all.",
            optional=True
        )
    ]
    options = [
        option(
            "directly",
            "d",
            description="If set, the mkdocs serve command will be run directly and not via tempdir",
            flag=True
        ),
        option(
            "webhooked",
            "w",
            description="If set mkdocs will be run in webhooked mode",
            flag=True
        )
    ]

    def handle(self):
      run_directly: bool = self.option("directly")
      repo_name: str = self.argument("repo")
      webhooked: bool = self.option("webhooked")

      if run_directly:
        dir_to_run_from = Path.cwd()
      else:
        dir_to_run_from = TEMP_DOCS_DIR
        prepare_temp_dir(repo_name)
        
      run_mkdocs(dir_to_run_from, bg = webhooked)
      
      if webhooked:
        run_webhook_server()


def get_application() -> Application:
  
  application = Application()
  application.add(RunMkDocsCommand())
  
  return application