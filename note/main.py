import os
import sys
import subprocess
from pathlib import Path
from pydantic import BaseModel
import fire

# default location
PATH_NOTES = os.getenv("PATH_NOTES", Path.home() / "notes" / "notes")
EDITOR = os.getenv('EDITOR', 'notepad' if os.name == 'nt' else 'vim')
FILE_EXTENSION = "md"


class Note(BaseModel):
    """note model"""
    repo: "Repository"
    index: int

    @property
    def path(self) -> Path:
        return self.repo.path / f"{self.index}.{FILE_EXTENSION}"

    def open(self, editor: str = EDITOR):
        subprocess.run([editor, str(self.path)])

    def read_content(self) -> str:
        with open(self.path, "r") as f:
            return f.read()

    def write_content(self, content: str) -> None:
        with open(self.path, "w") as f:
            f.write(content)


class Repository(BaseModel):
    """repository in which notes exist"""
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

    def get_last_note(self) -> Note:
        index_note = self.get_last_index()
        note = Note(repo=self, index=index_note)
        return note

    def get_new_note(self) -> Note:
        self.path.mkdir(parents=True, exist_ok=True)
        note = self.get_last_note()
        note.index += 1
        return note


def create_new_note():
    """Create and open a new note, default action."""
    repo = Repository()
    new_note = repo.get_new_note()
    new_note.open()


def list_notes():
    """List all notes."""
    repo = Repository()
    for note_file in repo.path.glob(f'*.{FILE_EXTENSION}'):
        print(note_file.stem)


def print_note(index: int = -1):
    """Read a specific note by index."""
    repo = Repository()
    if index <= -1:
        last = repo.get_last_index()
        index = last + index + 1
    note = Note(repo=repo, index=index)
    print(note.read_content())


def edit_note(index: int = -1):
    """Edit a specific note by index."""
    repo = Repository()
    if index <= -1:
        last = repo.get_last_index()
        index = last + index + 1
    note = Note(repo=repo, index=index)
    note.open()


def delete_note(index: int):
    """Delete a specific note by index."""
    repo = Repository()
    note = Note(repo=repo, index=index)
    os.remove(note.path)


def search_notes(term: str):
    """Search for a term in all notes."""
    repo = Repository()
    for note_file in repo.path.glob(f'*.{FILE_EXTENSION}'):
        note = Note(repo=repo, index=int(note_file.stem))
        content = note.read_content()
        if term.lower() in content.lower():
            print(f"Found in {note_file.stem}:")
            print(content)
            print("-" * 20)


def cli():
    """CLI entry point."""
    if len(sys.argv) == 1:
        create_new_note()
        exit()

    fire.Fire({
        'new': create_new_note,
        'list': list_notes,
        'print': print_note,
        'edit': edit_note,
        'delete': delete_note,
        'search': search_notes,
        'repository': Repository,
    })
