from sh import git 
import logging 
from atro_pylog import set_logger
from repo import get_repos
from git_helpers import pull_or_clone
from shutil import copyfile 
from constants import TEMP_DOCS_DIR


logging.info(f"Temp docs dir: {TEMP_DOCS_DIR.as_posix()}")


def prepare_temp_dir(repo_name: str | None = None):
    # Make a temp dir for docs
    copyfile("mkdocs.yml", TEMP_DOCS_DIR.as_posix() + "/mkdocs.yml")
    (TEMP_DOCS_DIR / "docs").mkdir(parents=True, exist_ok=True)
    (TEMP_DOCS_DIR / "repos").mkdir(parents=True, exist_ok=True)
    
    # Load yaml repos
    repos = get_repos(repo_name)
    
    # Clone and move docs if exist
    for repo in repos:
        pull_or_clone(TEMP_DOCS_DIR / "repos", repo.name, repo.path, repo.url)
        repos_docs_dir = TEMP_DOCS_DIR / "repos" / repo.path / "docs"
        if repos_docs_dir.exists() and repos_docs_dir.is_dir():
            repos_docs_dir.rename(TEMP_DOCS_DIR / "docs" / repo.name)
