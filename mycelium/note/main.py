import os
import sys
from pathlib import Path
from ..model import Note, Repository
import fire

# default location
PATH_NOTES = os.getenv("PATH_NOTES", Path.home() / "notes" / "notes")
EDITOR = os.getenv('EDITOR', 'notepad' if os.name == 'nt' else 'vim')
FILE_EXTENSION = "md"


def create_new_note():
    """Create and open a new note, default action."""
    repo = Repository()
    new_note = Note.new(repo)
    new_note.open()


def list_notes():
    """List all notes."""
    repo = Repository()
    print([str(i) for i in repo.get_list()])


def print_note(index: int = -1):
    """Read a specific note by index."""
    repo = Repository()
    note = Note.from_repository(repo=repo, index=index)
    print(note.read_content())


def edit_note(index: int = -1):
    """Edit a specific note by index."""
    repo = Repository()
    note = Note.from_repository(repo=repo, index=index)
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
