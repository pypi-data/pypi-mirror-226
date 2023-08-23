from pathlib import Path
import logging
from sh import git

# Git funcs
def pull_or_clone(temp_doc_dir: Path, name: str, path: Path, url: str):
  if not (temp_doc_dir / path).exists() or not (temp_doc_dir / path).is_dir():
    logging.info(f"Did not find repo {name} in {temp_doc_dir.as_posix()}. Cloning...")
    git.clone(url, path.as_posix(), _cwd=temp_doc_dir.as_posix())
  else:
    logging.info(f"Found repo {name} in {temp_doc_dir.as_posix()}. Pulling...")
    git.pull(_cwd=(temp_doc_dir / path).as_posix())

def get_current_repo_url() -> str:
  return git.remote("get-url", "origin").strip()

def get_current_repo_name() -> str:
  return get_current_repo_url().replace(".git", "").split("/")[-1]

def clean_and_pull_existing_repo(repo_path: Path):
  git.reset("--hard", _cwd=repo_path.as_posix())
  git.clean("-fxd", _cwd=repo_path.as_posix())
  git.pull(_cwd=repo_path.as_posix())