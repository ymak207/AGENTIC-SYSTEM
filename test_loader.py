from services.knowledge_service import KnowledgeService

service = KnowledgeService()

print()

print("=" * 80)

print("DOCUMENTS BEFORE")

print("=" * 80)

for doc in service.list_documents():

    print(doc)