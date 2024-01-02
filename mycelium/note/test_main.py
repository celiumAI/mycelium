from .main import create_new_note, list_notes, print_note, edit_note, search_notes

def test_create_new_note(mocker):
    """Create a new note."""
    mock = mocker.patch("subprocess.run")
    create_new_note()
    mock.assert_called_once()

def test_list_notes():
    """List all notes."""
    notes = list_notes()
    assert isinstance(notes, list)

def test_print_note():
    """Read a specific note by index."""
    note = print_note()
    assert isinstance(note, str)

def test_edit_note(mocker):
    """Edit a specific note by index."""
    mock = mocker.patch("subprocess.run")
    edit_note()
    assert mock.called

def test_search_notes():
    """Search for a term in all notes."""
    result = search_notes("test")
    assert isinstance(result, str)
