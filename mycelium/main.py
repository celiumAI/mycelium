from .model import Node, Repository
from .note.model import Note
from langchain.embeddings import OllamaEmbeddings
import numpy as np


BASE_URL_OLLAMA = "http://192.168.2.177:11434"
MODEL_EMBEDDING = "mycelium-embed"

OVERWRITE = True

class Embedding(Node):
    repo: Repository
    index: int

    @property
    def metadata(self) -> str:
        result = f"---\n"
        result += f"source: {self.path.stem}\n"
        result += "---\n"
        return result

    @property
    def meta(self) -> str:
        result = "```markdown\n"
        result += self.metadata
        result += self.read()
        result += "\n```\n"
        return result

    def write(self, content: list[float], overwrite=OVERWRITE) -> None:
        if not overwrite and self.exists:
            decision = input("embedding already exists, overwrite?")
            if decision.lower() not in ["y", "yes"]:
                return
        embedding = np.array(content)
        np.savetxt(self.path, embedding)

    @staticmethod
    def embed(node: Node) -> list[float]:
        embedder = OllamaEmbeddings(
            base_url=BASE_URL_OLLAMA, model=MODEL_EMBEDDING
        )
        content = node.read()
        embedding = embedder.embed_documents([content])[0]
        return embedding

def main():
    repo_notes = Repository()
    repo_mycelium = Repository(path=repo_notes.path.parent)
    repo_embeddings = Repository(
        path=repo_mycelium.path / "embeddings",
        extension="embed"
    )
    repo_embeddings.ensure_exists()
    for node in repo_notes.nodes:
        note = Note.from_repository(repo_notes, index=node.index)
        node_embedding = Embedding(
            index=node.index,
            repo=repo_embeddings,
        )
        if node_embedding.exists:
            print(f"skipped {node.index}")
            continue
        embedding = Embedding.embed(note)
        node_embedding.write(embedding)

if __name__ == "__main__":
    main()
