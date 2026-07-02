from knowledge.rag_loader import (
    RAGLoader
)

from knowledge.rag_cleaner import (
    RAGCleaner
)

from knowledge.rag_chunker import (
    RAGChunker
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

print()

print("TOTAL CHUNKS")

print("-" * 50)

print(len(chunks))

print()

print("CHUNK 1")

print("-" * 50)

print(chunks[0]["text"][-250:])

print()

print("=" * 70)

print()

print("CHUNK 2")

print("-" * 50)

print(chunks[1]["text"][:250])