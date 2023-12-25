from abc import abstractmethod

from typing import Any


class Driver:

    def __init__(self, config: dict) -> None:
        self._config = config

    @abstractmethod
    def find(self, _id: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def insert(self, _id: Any, _data: dict[str, Any]) -> Any:
        raise NotImplementedError

    @abstractmethod
    def update(self, _id: Any, _new_data: dict[str, Any]) -> Any:
        raise NotImplementedError

    @abstractmethod
    def delete(self, _id: Any) -> Any:
        raise NotImplementedError
