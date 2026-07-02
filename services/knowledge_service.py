from pathlib import Path
import shutil
from datetime import datetime

from knowledge.rag_loader import RAGLoader
from knowledge.rag_cleaner import RAGCleaner
from knowledge.rag_chunker import RAGChunker
from knowledge.rag_vector_store import RAGVectorStore


class KnowledgeService:

    def __init__(self):

        self.documents_folder = (
            Path("knowledge/documents")
        )

        self.loader = RAGLoader()

        self.cleaner = RAGCleaner()

        self.chunker = RAGChunker()

        self.vector_store = RAGVectorStore()

    # ------------------------------------------------

    def list_documents(self):

        vectors = self.vector_store.load_vectors()

        chunk_counts = {}

        for vector in vectors:

            document = vector["document"]

            chunk_counts[document] = (
                chunk_counts.get(document, 0) + 1
            )

        documents = []

        for pdf in self.documents_folder.glob("*.pdf"):

            documents.append(
                {
                    "name": pdf.name,
                    "size_mb": round(
                        pdf.stat().st_size / 1024 / 1024,
                        2
                    ),
                    "chunks": chunk_counts.get(
                        pdf.name,
                        0
                    ),
                    "modified": datetime.fromtimestamp(
                        pdf.stat().st_mtime
                    ).strftime("%Y-%m-%d %H:%M"),
                    "status": (
                        "Indexed"
                        if pdf.name in chunk_counts
                        else "Not Indexed"
                    )
                }
            )

        return sorted(
            documents,
            key=lambda x: x["name"]
        )

    # ------------------------------------------------

    def upload_document(
        self,
        uploaded_file
    ):

        destination = (
            self.documents_folder
            / uploaded_file.name
        )

        with open(
            destination,
            "wb"
        ) as file:

            shutil.copyfileobj(
                uploaded_file,
                file
            )

        return self.rebuild_index()

    # ------------------------------------------------

    def delete_document(
        self,
        filename
    ):

        pdf = (
            self.documents_folder
            / filename
        )

        if pdf.exists():

            pdf.unlink()

        return self.rebuild_index()

    # ------------------------------------------------

    def rebuild_index(self):

        documents = self.loader.load_directory(
            str(self.documents_folder)
        )

        documents = self.cleaner.clean(
            documents
        )

        chunks = self.chunker.chunk(
            documents
        )

        self.vector_store.build_index(
            chunks
        )

        return {
            "documents": len(documents),
            "chunks": len(chunks)
        }