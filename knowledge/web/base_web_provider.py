from abc import ABC
from abc import abstractmethod


class BaseWebProvider(ABC):

    @abstractmethod
    def search(
        self,
        query: str,
        top_k: int = 3
    ):
        pass