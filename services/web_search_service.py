from knowledge.web.duckduckgo_provider import (
    DuckDuckGoProvider
)


class WebSearchService:

    def __init__(self):

        self.provider = DuckDuckGoProvider()

    def search(

        self,

        query,

        top_k=3

    ):

        return self.provider.search(

            query,

            top_k

        )