from typing import Optional
from pydantic import BaseModel, Field

from backend.app.api.utils.cnpj import is_cnpj_str_valid
from .base import BatchModel
from .misc import LimitOffsetParams


class CNPJBatch(BatchModel):
    pass


class CNPJQueryParams(LimitOffsetParams):
    state_abbrev: str = Field("")
    city_name: str = Field("")
    zipcode: str = Field("")
    cnae_code: str = Field("")
    is_all: bool = Field(True)


class ModeloSimplesSimei(BaseModel):
    optante: bool = False
    data_opcao: Optional[str]
    data_exclusao: Optional[str]


class CNPJ:
    def __init__(self, basico: str, ordem: str, digitos_verificadores: str):
        try:
            self.basico_int: str = int(basico)
        except ValueError as exc:
            raise ValueError(
                "Digits 'basico' contains non-numeric characters."
            ) from exc

        try:
            self.ordem_int = int(ordem)
        except ValueError as exc:
            raise ValueError("Digits 'ordem' contains non-numeric characters.") from exc

        try:
            self.digitos_verificadores_int = int(digitos_verificadores)
        except ValueError as exc:
            raise ValueError(
                "Digits 'digitos_verificadores' contains non-numeric characters."
            ) from exc

        self.basico_str = str(basico).zfill(8)
        self.ordem_str = str(ordem).zfill(4)
        self.digitos_verificadores_str = str(digitos_verificadores).zfill(2)

    def is_valid_dict(self):
        """
        Validates a given CNPJ number and returns a dictionary with results.

        Args:
            cnpj: The CNPJ number to validate (string).

        Returns:
            A dictionary with keys:
                'is_valid': True if the CNPJ is valid, False otherwise.
                'reason': A string explaining the validation failure (empty if valid).
        """
        cnpj = f"{self.basico_str}{self.ordem_str}{self.digitos_verificadores_str}"

        return is_cnpj_str_valid(cnpj)

    def __dict__(self):
        is_valid_dict = self.is_valid_dict()

        return {
            "basico": self.basico_str,
            "ordem": self.ordem_str,
            "digitos_verificadores": self.digitos_verificadores_str,
            "is_valid": is_valid_dict["is_valid"],
            "reason": is_valid_dict["reason"],
        }

    def to_tuple(self):
        return (
            self.basico_str,
            self.ordem_str,
            self.digitos_verificadores_str,
        )

    def to_raw(self):
        return f"{self.basico_str}{self.ordem_str}{self.digitos_verificadores_str}"

    def __str__(self):
        basico = f"{self.basico_str[:2]}.{self.basico_str[2:5]}.{self.basico_str[5:8]}"
        ordem = f"{self.ordem_str}"
        digitos_verificadores = f"{self.digitos_verificadores_str}"

        return f"{basico}/{ordem}-{digitos_verificadores}"

    def __repr__(self) -> str:
        return self.__str__()
