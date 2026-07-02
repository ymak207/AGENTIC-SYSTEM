from knowledge.rag_loader import RAGLoader
from knowledge.rag_chunker import RAGChunker

loader = RAGLoader()

documents = loader.load_directory(
    "knowledge/documents"
)

chunker = RAGChunker()

chunks = chunker.chunk(
    documents
)

print()

print("TOTAL CHUNKS")

print(len(chunks))

print()

print(chunks[0])

print()

print(chunks[1])