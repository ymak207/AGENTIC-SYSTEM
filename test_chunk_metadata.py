from knowledge.rag_loader import RAGLoader
from knowledge.rag_cleaner import RAGCleaner
from knowledge.rag_chunker import RAGChunker


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

print("FIRST CHUNK")

print("-" * 50)

print(chunks[0])

print()

print("=" * 70)

print()

print("SECOND CHUNK")

print("-" * 50)

print(chunks[1])