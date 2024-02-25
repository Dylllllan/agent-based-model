from abc import abstractmethod, ABC


class ISerializable(ABC):
    @abstractmethod
    def toDict(self) -> dict:
        raise NotImplementedError
