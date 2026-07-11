from services.web_search_service import (
    WebSearchService
)

service = WebSearchService()

results = service.search(

    "Latest AWS announcements",

    top_k=3

)

print()

print("=" * 80)

print("WEB RESULTS")

print("=" * 80)

print()

for item in results:

    print("Title :", item["title"])

    print("URL   :", item["url"])

    print("Text  :", item["content"])

    print("-" * 80)