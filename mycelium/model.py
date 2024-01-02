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
        return self.repo.path / f"{self.index}.{self.repo.extension}"

    @property
    def raw(self):
        """printable raw content of the node"""
        raise NotImplementedError()

    @property
    def meta(self) -> str:
        """printable verbose content of the node"""
        raise NotImplementedError()

    @property
    def edit(self) -> str:
        """edit the raw content of the node"""
        raise NotImplementedError()

    @classmethod
    def from_repository(cls, repo: "Repository", index=-1) -> "Node":
        """load node from repo"""
        raise NotImplementedError()

    @classmethod
    def new(cls, repo: "Repository") -> "Node":
        """create a new node in repo"""
        raise NotImplementedError()

class Note(Node):
    """note model"""
    def meta(self) -> str:
        result = "```markdown\n"
        result += f"---\n"
        result += f"note: {self.path.stem}\n"
        result += "---\n\n"
        result += self.raw
        result += "\n```\n"
        return result

    def __str__(self) -> str:
        return self.raw

    @property
    def raw(self) -> str:
        return self.read()

    def edit(self, editor: str = EDITOR):
        subprocess.run([editor, str(self.path)])

    def read(self) -> str:
        with open(self.path, "r") as f:
            return f.read()

    def write(self) -> None:
        with open(self.path, "w") as f:
            f.write(str(self))

    @classmethod
    def from_repository(cls, repo: "Repository", index=-1) -> "Note":
        if index <= -1:
            last = repo.get_last_index()
            index = last + index + 1
        note = cls(index=index, repo=repo)
        return note

    @classmethod
    def new(cls, repo: "Repository") -> "Note":
        last = repo.get_last_index()
        index = last + 1
        note = cls(index=index, repo=repo)
        return note


class Repository(BaseModel):
    """
    repository in which nodes exist
    you can think of it like a color channel in an image
    """
    path: Path = PATH_NOTES
    extension: str = FILE_EXTENSION

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
            self.index_nodes,
            default=0
        )
        return highest_num

    @property
    def index_nodes(self) -> list[int]:
        elements = list(
            int(p.stem) for p in self.path.glob(
                f"*.{self.extension}"
            )
        )
        elements = sorted(elements)
        return elements

    @property
    def nodes(self) -> list:
        indices = self.index_nodes
        if self.extension == "md":
            elements = [
                Note.from_repository(
                    self, index
                )
                for index in indices
            ]
        return elements

    def new_node(self) -> Node | Note:
        if self.extension == "md":
            return Note.new(self)
        if self.extension == "embedding":
            return Node.new(self)
