class RAGChunker:

    def chunk(
        self,
        documents,
        chunk_size=500,
        overlap=100
    ):

        chunks = []

        for document in documents:

            words = document["text"].split()

            start = 0

            chunk_number = 1

            while start < len(words):

                end = start + chunk_size

                chunk_words = words[start:end]

                chunk_text = " ".join(chunk_words)

                chunks.append(
                    {
                        "document": document["name"],
                        "chunk": chunk_number,
                        "chunk_id": (
                            f"{document['name']}_{chunk_number}"
                        ),
                        "word_count": len(chunk_words),
                        "text": chunk_text
                    }
                )

                chunk_number += 1

                start += (
                    chunk_size - overlap
                )

        return chunks