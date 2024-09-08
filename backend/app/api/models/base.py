from typing import Union, List

from pydantic import BaseModel


class BatchModel(BaseModel):
    batch: List[Union[str, int]]
