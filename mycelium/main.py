from llama_index import VectorStoreIndex
from .embed import embed_nodes, Embedding
from .model import Repository
from .note.model import Note
from annoy import AnnoyIndex

N_TREES = 10

def get_index(embeddings: list[Embedding]):
    f = len(embeddings[0].read())

    t = AnnoyIndex(f, 'angular')
    for i in range(len(embeddings)):
        v = embeddings[i].read()
        t.add_item(i, v)

    t.build(20) # 10 trees

    return t

def main():
    repo_notes = Repository(node_type=Note)
    repo_embeddings = embed_nodes(repo_notes)
    nodes_embedded = repo_embeddings.nodes
    index = get_index(nodes_embedded)
    note = repo_notes.nodes[0]
    note_embedding = repo_embeddings.nodes[0]
    similar = index.get_nns_by_vector(note_embedding.read(), 3)
    for i in similar:
        note_similar = repo_notes.nodes[i+1]
        print(repr(note_similar.read()))

    print(note.read())


if __name__ == "__main__":
    main()
