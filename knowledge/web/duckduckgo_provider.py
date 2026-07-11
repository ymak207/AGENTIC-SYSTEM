from ddgs import DDGS

from knowledge.web.base_web_provider import (
    BaseWebProvider
)


class DuckDuckGoProvider(BaseWebProvider):

    def search(
        self,
        query,
        top_k=3
    ):

        results = []

        try:

            with DDGS() as ddgs:

                response = ddgs.text(

                    query,

                    max_results=top_k

                )

                for item in response:

                    results.append(

                        {

                            "source": "web",

                            "title": item.get("title"),

                            "url": item.get("href"),

                            "content": item.get("body"),

                            "score": 1.0,

                            "metadata": {}

                        }

                    )

        except Exception as ex:

            print(
                "DuckDuckGo Search Error:",
                ex
            )

        return results