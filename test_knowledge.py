from services.knowledge_service import (
    KnowledgeService
)

service = KnowledgeService()

documents = service.list_documents()

print()

print("=" * 80)
print("DOCUMENTS")
print("=" * 80)

for doc in documents:

    print()

    print("Name      :", doc["name"])
    print("Size (MB) :", doc["size_mb"])
    print("Chunks    :", doc["chunks"])
    print("Modified  :", doc["modified"])
    print("Status    :", doc["status"])

print()

print("=" * 80)
print("REBUILD")
print("=" * 80)

print()

print(
    service.rebuild_index()
)