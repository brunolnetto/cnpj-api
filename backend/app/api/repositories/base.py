from abc import ABC
from typing import Any
from typing import Dict
from typing import List


class BaseRepository(ABC):
    def __init__(self, session):
        self.session = session

    def create(self, data: Dict[str, Any]) -> Any:
        raise NotImplementedError()

    def update(self, item_id: Any, data: Dict[str, Any]) -> Any | None:
        raise NotImplementedError()

    def get_by_id(self, item_id: Any) -> Any | None:
        raise NotImplementedError()

    def delete_by_id(self, item_id: Any) -> bool:
        raise NotImplementedError()

    def get_all(self, limit: int = 100, offset: int = 0) -> List[Any]:
        raise NotImplementedError()
