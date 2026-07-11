from services.web_search_service import (
    WebSearchService
)


class WebProvider:

    def __init__(self):

        self.web = WebSearchService()

    # -------------------------------------------------

    def retrieve(
        self,
        query,
        state
    ):

        try:

            results = self.web.search(
                query,
                top_k=3
            )

        except Exception as ex:

            print(
                "Web Provider Error:",
                ex
            )

            results = []

        state.knowledge["web"] = results

        state.add_trace(
            f"Web Retrieved ({len(results)})"
        )