from abc import ABC, abstractmethod


class BaseKnowledgeProvider(ABC):

    @abstractmethod
    def retrieve(
        self,
        query: str,
        state
    ):
        pass