from model import Node, Note, Repository
from langchain.embeddings import OllamaEmbeddings


BASE_URL_OLLAMA = "http://192.168.2.177:11434"
MODEL_EMBEDDING = "mycelium-embed"


class Embedding(Node):
    repo: Repository
    index: int


def embed_note(note: Note):
    embedder = OllamaEmbeddings(
        base_url=BASE_URL_OLLAMA, model=MODEL_EMBEDDING
    )
    content = note.content
    embedding = embedder.embed_documents([content])[0]
    print(f"embedding dim: {len(embedding)}")
    return embedding


def embed_notes(repo: Repository) -> list[float]:
    embeddings = []
    for note in repo.elements():
        embeddings.append(embed_note(note))
    return embeddings


def save_embedding(repo_embeddings, embedding, index):
    print(repo_embeddings)


def main():
    repo_notes = Repository()
    repo_mycelium = Repository(path=repo_notes.path.parent)
    repo_embeddings = Repository(
        path=repo_mycelium.path / "embeddings",
        extension="embed"
    )
    repo_embeddings.ensure_exists()
    note = Note.from_repository(repo_notes)
    print(repo_notes)
    print(repo_mycelium)
    print(repo_embeddings)
    print(note)
    embedding = embed_note(note)

if __name__ == "__main__":
    main()
