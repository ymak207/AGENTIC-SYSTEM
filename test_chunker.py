from knowledge.rag_chunker import (
    RAGChunker
)

chunker = RAGChunker()

text = (
    "AWS is a cloud platform. "
    * 700
)

chunks = chunker.chunk(text)

print()

print("TOTAL CHUNKS")

print(len(chunks))

print()

for i, chunk in enumerate(chunks, start=1):

    print(
        f"Chunk {i}: "
        f"{len(chunk.split())} words"
    )