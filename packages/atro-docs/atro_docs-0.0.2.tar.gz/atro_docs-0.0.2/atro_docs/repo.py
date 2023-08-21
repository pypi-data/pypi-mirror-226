from pydantic import BaseModel, computed_field
from pathlib import Path
from constants import REPOS_YAML_FILE_NAME
from git_helpers import get_current_repo_url, get_current_repo_name
import yaml

class Repo(BaseModel):
    path: Path
    url: str

    @computed_field
    @property
    def name(self) -> str:
        return self.path.parts[0]

def get_repos(repo_name: str | None = None):
    # Load yaml repos
    if Path(REPOS_YAML_FILE_NAME).exists():
        with open(REPOS_YAML_FILE_NAME, 'r') as file:
            repos = [Repo(**repo) for repo in yaml.safe_load(file)["Repos"]]
    else:
        repos = [Repo(path = Path(get_current_repo_name()), url = get_current_repo_url())]   
    
    if repo_name:
        repos = [repo for repo in repos if repo.name.lower() == repo_name.lower()]
    return repos 