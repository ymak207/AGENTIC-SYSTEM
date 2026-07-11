from abc import ABC
from abc import abstractmethod


class BaseCapability(ABC):

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def execute(
        self,
        request,
        context
    ):
        pass