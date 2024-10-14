from abc import ABC
from typing import List, Optional, Dict, Any


class BaseRepository(ABC):
    def __init__(self, session):
        self.session = session

    async def create(self, data: Dict[str, Any]) -> Any:
        raise NotImplementedError()

    async def update(self, item_id: Any, data: Dict[str, Any]) -> Optional[Any]:
        raise NotImplementedError()

    async def get_by_id(self, item_id: Any) -> Optional[Any]:
        raise NotImplementedError()

    async def delete_by_id(self, item_id: Any) -> bool:
        raise NotImplementedError()

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[Any]:
        raise NotImplementedError()
