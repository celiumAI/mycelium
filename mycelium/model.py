import os
import subprocess
from pathlib import Path
from pydantic import BaseModel

# default location
PATH_NOTES = os.getenv("PATH_NOTES", Path.home() / "notes" / "notes")
EDITOR = os.getenv('EDITOR', 'notepad' if os.name == 'nt' else 'vim')
FILE_EXTENSION = "md"


class Node(BaseModel):
    """a node in a hyphal network"""
    repo: "Repository"
    index: int

    @property
    def path(self) -> Path:
        raise NotImplementedError("you need to implement a path property")

    @property
    def content(self) -> str:
        raise NotImplementedError("you need to implement a content property")


class Note(Node):
    """note model"""
    @property
    def path(self) -> Path:
        return self.repo.path / f"{self.index}.{FILE_EXTENSION}"

    @property
    def content(self) -> str:
        return self.read_content()

    def open(self, editor: str = EDITOR):
        subprocess.run([editor, str(self.path)])

    def read_content(self) -> str:
        with open(self.path, "r") as f:
            return f.read()

    def write_content(self, content: str) -> None:
        with open(self.path, "w") as f:
            f.write(content)

    @classmethod
    def from_repository(cls, repo: "Repository") -> "Note":
        index = repo.get_last_index() + 1
        note = cls(index=index, repo=repo)
        return note


class Repository(BaseModel):
    """
    repository in which nodes exist
    you can think of it like a color channel in an image
    """
    path: Path = PATH_NOTES

    def ensure_exists(self, autocreate: bool = False) -> None:
        msg = "The specified path does not exist."
        if not self.path.is_dir():
            if not autocreate:
                user_input = input(
                    'Path does not exist. Do you want to create it? (y/n): '
                )
                if user_input.lower() == 'y':
                    self.path.mkdir(parents=True, exist_ok=True)
                    msg = "The specified path has been created."
            else:
                self.path.mkdir(parents=True, exist_ok=True)
        if not self.path.is_dir():
            raise ValueError(msg)

    def get_last_index(self) -> int:
        highest_num = max(
            (
                int(p.stem) for p in self.path.glob(
                    f'*.{FILE_EXTENSION}'
                )
                if p.stem.isdigit()
            ),
            default=0
        )
        return highest_num
