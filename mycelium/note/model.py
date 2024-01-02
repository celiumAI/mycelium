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
    def meta(self) -> str:
        result = "```markdown\n"
        result += f"---\n"
        result += f"note: {self.path.stem}\n"
        result += "---\n\n"
        result += self.raw
        result += "\n```\n"
        return result

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
    def new(cls, repo: Repository) -> "Note":
        index = repo.get_last_index() + 1
        note = Note(repo=repo, index=index)
        return note
