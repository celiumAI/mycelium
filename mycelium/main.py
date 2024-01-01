from model import Note, Repository


def embed_note(note: Note):
    content = note.content
    print(content)


if __name__ == "__main__":
    repo_notes = Repository()
    repo_mycelium = Repository(path=repo_notes.path.parent)
    repo_embeddings = Repository(path=repo_mycelium.path / "embeddings")
    repo_embeddings.ensure_exists()
    note = Note.from_repository(repo_notes)
    print(repo_notes)
    print(repo_mycelium)
    print(repo_embeddings)
    print(note)
    embed_note(note)
