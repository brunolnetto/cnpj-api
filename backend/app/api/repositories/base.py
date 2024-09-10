from abc import ABC
from typing import List, Optional, Dict, Any


class BaseRepository(ABC):
    def __init__(self, session):
        self.session = session

    def create(self, data: Dict[str, Any]) -> Any:
        raise NotImplementedError()

    def update(self, id: Any, data: Dict[str, Any]) -> Optional[Any]:
        raise NotImplementedError()

    def get_by_id(self, id: Any) -> Optional[Any]:
        raise NotImplementedError()

    def delete_by_id(self, id: Any) -> bool:
        raise NotImplementedError()

    def get_all(self, limit: int = 100, offset: int = 0) -> List[Any]:
        raise NotImplementedError()
