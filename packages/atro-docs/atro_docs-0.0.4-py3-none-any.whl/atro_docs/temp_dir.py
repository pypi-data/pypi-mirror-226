import logging

import mkdocs 
from repo import get_repos
from git_helpers import pull_or_clone, clean_and_pull_existing_repo
from shutil import copyfile 
from constants import TEMP_DOCS_DIR
from pathlib import Path
import shutil

logging.info(f"Temp docs dir: {TEMP_DOCS_DIR.as_posix()}")

def wipe_dir(dir_path: Path):
    # Iterate over items inside the directory
    for item in dir_path.iterdir():
        if item.is_file():
            item.unlink()  # Remove the file
        elif item.is_dir():
            shutil.rmtree(item)  # Remove the directory

def reset_already_existing_repos(repo_name: str | None = None):
    # Load yaml repos
    repos = get_repos(repo_name)
    
    # Clone and move docs if exist
    for repo in repos:
        repo_path = TEMP_DOCS_DIR / "repos" / repo.path
        if repo_path.exists():
            clean_and_pull_existing_repo(repo_path)

def fill_up_docs_and_mkdocs_yml(repo_name: str | None = None):
    # Load yaml repos
    repos = get_repos(repo_name)
    mkdocs_yml_path = TEMP_DOCS_DIR / "mkdocs.yml"
    
    if mkdocs_yml_path.exists():
        mkdocs_yml_path.unlink()
    
    for repo in repos:
        repos_docs_dir = TEMP_DOCS_DIR / "repos" / repo.path / "docs"
        original_docs_dir = TEMP_DOCS_DIR / "docs" / repo.name
        
        if original_docs_dir.exists() and original_docs_dir.is_dir():
            wipe_dir(original_docs_dir)
        
        if repos_docs_dir.exists() and repos_docs_dir.is_dir():
            repos_docs_dir.rename(TEMP_DOCS_DIR / "docs" / repo.name)

        if not mkdocs_yml_path.exists() and (TEMP_DOCS_DIR / "repos" / repo.path / "mkdocs.yml").exists():
            (TEMP_DOCS_DIR / "repos" / repo.path / "mkdocs.yml").rename(mkdocs_yml_path)
            
def prepare_temp_dir(repo_name: str | None = None):
    # Make a temp dir for docs
    (TEMP_DOCS_DIR / "docs").mkdir(parents=True, exist_ok=True)
    (TEMP_DOCS_DIR / "repos").mkdir(parents=True, exist_ok=True)
    
    # Load yaml repos
    repos = get_repos(repo_name)
    
    # Clone and move docs if exist
    for repo in repos:
        pull_or_clone(TEMP_DOCS_DIR / "repos", repo.name, repo.path, repo.url)
        
    fill_up_docs_and_mkdocs_yml(repo_name)