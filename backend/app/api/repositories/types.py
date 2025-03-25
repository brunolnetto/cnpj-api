from typing import Any
from typing import Dict
from typing import List
from typing import Union

from backend.app.api.models.cnpj import CNPJ

# Types
CNPJList = List[CNPJ]
JSON = Dict[str, Any]
CodeType = Union[str, int]
CodeListType = List[CodeType]
PayloadType = Dict[str, str]
