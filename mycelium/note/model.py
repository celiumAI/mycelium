import os
import subprocess
from pathlib import Path

from ..model import Node, Repository

# default location
PATH_NOTES = os.getenv("PATH_NOTES", Path.home() / "notes" / "notes")
EDITOR = os.getenv('EDITOR', 'notepad' if os.name == 'nt' else 'vim')
FILE_EXTENSION = "md"

class Note(Node):
    """note model"""

    @property
    def metadata(self) -> str:
        result = f"---\n"
        result += f"note: {self.path.stem}\n"
        result += "---\n"
        return result

    @property
    def meta(self) -> str:
        result = "```markdown\n"
        result += self.metadata
        result += self.read()
        result += "\n```\n"
        return result

    def edit(self, editor: str = EDITOR):
        subprocess.run([editor, str(self.path)])

    def read(self) -> str:
        with open(self.path, "r") as f:
            return f.read()

    def write(self, content) -> None:
        with open(self.path, "w") as f:
            f.write(content)

    @classmethod
    def new(cls, repo: Repository) -> "Note":
        index = repo.get_last_index() + 1
        note = Note(repo=repo, index=index)
        return note

    @staticmethod
    def from_repository(repo: "Repository", index=-1) -> "Note":
        """load node from repo"""
        if index <= -1:
            last = repo.get_last_index()
            index = last + index + 1
        note = Note(index=index, repo=repo)
        return note
