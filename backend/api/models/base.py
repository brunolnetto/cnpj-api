from pydantic import BaseModel
from typing import Union, List

class BatchModel(BaseModel):
    batch: List[Union[str, int]]