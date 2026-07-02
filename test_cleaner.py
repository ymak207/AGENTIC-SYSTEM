from knowledge.rag_loader import RAGLoader
from knowledge.rag_cleaner import RAGCleaner

loader = RAGLoader()

documents = loader.load_directory(
    "knowledge/documents"
)

cleaner = RAGCleaner()

cleaned_documents = cleaner.clean(
    documents
)

print()

print("DOCUMENT")

print("-" * 50)

print(cleaned_documents[0]["name"])

print()

print(cleaned_documents[0]["text"][:1500])