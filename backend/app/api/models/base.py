from typing import List
from typing import Union

from pydantic import BaseModel


class BatchModel(BaseModel):
    batch: List[Union[str, int]]
