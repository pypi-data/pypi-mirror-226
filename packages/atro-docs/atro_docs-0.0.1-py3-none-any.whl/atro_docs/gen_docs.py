from typing import Callable
from pydantic import BaseModel, computed_field
from pathlib import Path
from abc import ABC, abstractmethod
from atro_docs.git_helpers import get_current_repo_name
import re 

class DocsGenerator(BaseModel, ABC):
  repo_name: str = get_current_repo_name().strip().lower().capitalize()
  base_dir: Path
  docs_dir: Path
  ProcessedDocsDirs: list[Path] = []
  
  @computed_field()
  def DocsDirs(self) -> list[Path]:
    return self.get_all_docs_files_paths()
  
  @abstractmethod
  def get_all_docs_files_paths(self) -> list[Path]:
    ...

  @abstractmethod
  def files_to_include_in_doc_file(self, file_path: Path) -> list[Path]:
    ...

  @staticmethod
  def insert_dashes(s):
      return re.sub(r'(?<!^)([A-Z])', r'-\1', s)
    
  @staticmethod
  def pretify_name(name: str) -> str:
      name = DocsGenerator.insert_dashes(name)
      lst = [nm.capitalize() for nm in name.split("-")]
      return " ".join(lst)
  
  def get_name_content(self, file_path: Path, doc_aut_get_prefix: str) -> str:
    content = []
    name = file_path.name
    
    content.append(f"<!-- auto-generated-{doc_aut_get_prefix} -->")
    content.append(f"# {DocsGenerator.pretify_name(name)}")
    content.append(f"<!-- auto-generated-{doc_aut_get_prefix} -->")
    
    return "\n".join(content)

  def get_files_content(self, file_path: Path, doc_aut_get_prefix: str) -> str:
    files_to_include_in_doc_file = self.files_to_include_in_doc_file(file_path)
    content = []
    content.append(f"<!-- auto-generated-{doc_aut_get_prefix} -->")
    content.append("## Files\n")
    
    for file_data_path in files_to_include_in_doc_file:
      match (file_data_path.suffix):
        case ".yaml":
          content.append(self.get_yaml_file_snippet(file_data_path))
        case ".md":
          content.append(self.get_md_file_snippet(file_data_path))
    
    content.append(f"<!-- auto-generated-{doc_aut_get_prefix} -->")
    
    return "\n".join(content) 
  
  def get_readme_content(self, file_path: Path, doc_aut_get_prefix: str) -> str:
    
    files_to_include_in_doc_file = self.files_to_include_in_doc_file(file_path)
    par_dirs = [file_path.parent for file_path in files_to_include_in_doc_file]
    par_dirs = list(set(par_dirs))
    content = []
    
    for par_dir in par_dirs:
      if (par_dir / "README.md").exists():
        content.append(self.get_md_file_snippet(par_dir / "README.md"))
    
    if len(content) > 0:
      content.insert(0, f"<!-- auto-generated-{doc_aut_get_prefix} -->")
      content.append(f"<!-- auto-generated-{doc_aut_get_prefix} -->")
    
    return "\n".join(content)
    
  
  def get_yaml_file_snippet(self , yaml_file: Path) -> str:
    content = []
    content.append(f"### {yaml_file.name}")
    content.append("~~~yaml")
    relative_prefix = self.get_relative_prefix(yaml_file)
    relative_path = f"{relative_prefix}{yaml_file.relative_to(self.base_dir)}"
    content.append(f"{{% include \"{relative_path}\" %}}")
    content.append("~~~\n")
    
    return "\n".join(content)

  def get_relative_prefix(self, file_path: Path) -> str:
    depth = len(file_path.parts)
    return "../" * depth + f"repos/{self.repo_name}/"
          
  def get_md_file_snippet(self, md_file: Path) -> str:
    relative_prefix = self.get_relative_prefix(md_file)
    relative_path = f"{relative_prefix}{md_file.relative_to(self.base_dir)}"

    return '{% include-markdown "' +  relative_path + '" %}'
  
  
  
  def write_to_doc_file(self, file_path: Path, func_content: Callable[[Path, str], str], doc_aut_get_prefix: str, downNotUp: bool = True) -> None:    
    content = func_content(file_path, doc_aut_get_prefix)
    
    if content == "" or content is None:
      return
    
    if file_path.is_dir():
      file_path = Path(file_path.as_posix() + ".md")
    else:
      file_path = Path("/".join(file_path.as_posix().split(".")[:-1]) + ".md")
    
    file_path = Path(self.docs_dir / file_path)
    if len(file_path.parts) > 1:
      file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Try to read the file's content if it exists
    lines = []
    if file_path.exists():
      with open(file_path, 'r') as f:
        lines = f.readlines()

    # Find the start and end indices
    start_index = None
    end_index = None

    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line == f"<!-- auto-generated-{doc_aut_get_prefix} -->":
            if start_index is None:
                start_index = i
            else:
                end_index = i
                break

    # If one marker is found but not the other, raise an error
    if (start_index is None and end_index is not None) or (start_index is not None and end_index is None):
        raise ValueError("Found only one auto-generated marker in the file!")

    # Replace content between the markers, or append to the end if no markers found
    if start_index is not None and end_index is not None:
      del lines[start_index:end_index+1]
      
      if downNotUp and len(lines) > start_index - 1 and lines[start_index - 1].strip() != "":
        print(lines[start_index - 1].strip())
        lines.insert(start_index, "\n")
        start_index += 1
        
      lines.insert(start_index, content + "\n")
      
    else:
      if downNotUp:
        lines.append(content + "\n")
      else:
        lines.insert(0, content + "\n")


    # Write modified lines back to the file (or create a new one if it doesn't exist)
    with open(file_path, 'w') as f:
        f.writelines(lines)

  def write(self, file_path: Path) -> None:
    self.write_to_doc_file(file_path, self.get_files_content, "files")
    
    # order here matters, readme should be written title so first we pop readme at the top and then tittle (so that tittle is at the top)
    self.write_to_doc_file(file_path, self.get_readme_content, "readme", downNotUp=False)
    self.write_to_doc_file(file_path, self.get_name_content, "title", downNotUp=False)
    
  
  def write_all_docs_files(self) -> None:
    all_doc_paths = self.get_all_docs_files_paths()
      
    for file_path in all_doc_paths:
      self.write(file_path)
  