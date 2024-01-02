import os
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
    def exists(self) -> bool:
        return self.path.exists()

    @property
    def metadata(self) -> str:
        """printable verbose metadata of the node"""
        raise NotImplementedError()

    @property
    def meta(self) -> str:
        """printable verbose content of the node"""
        raise NotImplementedError()

    def edit(self) -> str:
        """edit the raw content of the node"""
        raise NotImplementedError()

    @classmethod
    def from_repository(cls, repo: "Repository", index=-1):
        """load node from repo"""
        if index <= -1:
            last = repo.get_last_index()
            index = last + index + 1
        note = cls(index=index, repo=repo)
        return note

    @classmethod
    def new(cls, repo: "Repository"):
        """create a new node in repo"""
        raise NotImplementedError()

    def write(self):
        """write node to file"""
        raise NotImplementedError()

    def read(self):
        """read raw content of the node"""
        raise NotImplementedError()

class Repository(BaseModel):
    """
    repository in which nodes exist
    you can think of it like a color channel in an image
    """
    path: Path = PATH_NOTES
    extension: str = FILE_EXTENSION
    node_type: type[Node]

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
    def nodes(self) -> list["node_type"]:
        indices = self.index_nodes
        elements = [
            self.node_type.from_repository(
                self, index
            )
            for index in indices
        ]
        return elements

    def new_node(self) -> "node_type":
        return self.node_type.new(self)
