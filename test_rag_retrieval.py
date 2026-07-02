from knowledge.rag_loader import (
    RAGLoader
)

from knowledge.rag_cleaner import (
    RAGCleaner
)

from knowledge.rag_chunker import (
    RAGChunker
)

from knowledge.rag_vector_store import (
    RAGVectorStore
)


loader = RAGLoader()

documents = loader.load_directory(
    "knowledge/documents"
)

cleaner = RAGCleaner()

documents = cleaner.clean(
    documents
)

chunker = RAGChunker()

chunks = chunker.chunk(
    documents
)

vector_store = RAGVectorStore()

vector_store.build_index(
    chunks
)

results = vector_store.search(
    "What are the six pillars of the AWS Well-Architected Framework?"
)

print()

print("RESULTS")

print("-" * 70)

for result in results:

    print()

    print("Document   :", result["document"])

    print("Chunk      :", result["chunk"])

    print("Chunk ID   :", result["chunk_id"])

    print("Score      :", result["score"])

    print("Words      :", result["word_count"])

    print()

    print(result["text"][:700])

    print()

    print("=" * 70)