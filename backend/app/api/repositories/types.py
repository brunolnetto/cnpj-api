from typing import Tuple, Dict, Union, List, Any, Optional
from backend.app.api.models.cnpj import CNPJ

# Types
CNPJList = List[CNPJ]
JSON = Dict[str, Any]
CodeType = Union[str, int]
CodeListType = List[CodeType]
PayloadType = Dict[str, str]