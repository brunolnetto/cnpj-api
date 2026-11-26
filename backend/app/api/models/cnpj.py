from typing import Optional
from datetime import date
from pydantic import BaseModel, Field, model_validator, field_validator

from backend.app.api.utils.cnpj import is_cnpj_str_valid
from .base import BatchModel
from .misc import LimitOffsetParams


class CNPJBatch(BatchModel):
    pass


class CNPJQueryParams(LimitOffsetParams):
    """Query parameters for filtering CNPJ data."""

    zipcode: Optional[str] = Field(
        None, description="8-digit ZIP code to filter the data"
    )
    city_name: Optional[str] = Field(None, description="City name to filter the data")
    state_abbrev: Optional[str] = Field(
        None, description="State abbreviation (e.g., 'SP' for São Paulo)"
    )
    activity_start_date: Optional[date] = Field(
        None, description="The date when the activity started."
    )
    only_headquarters: Optional[bool] = Field(
        False, description="Flag to return only headquarters records"
    )
    cnae_code: Optional[str] = Field(None, description="CNAE code to filter the data")
    has_secondary_cnae: bool = Field(True, description="Flag to return all records")

    @field_validator("zipcode")
    @classmethod
    def validate_zipcode(cls, value: str):
        """
        Normalize the ZIP code to the 8 digits stored in the database.

        Accepts "01001000" and "01001-000", and 7 digits when the leading zero
        was lost (e.g. the CEP went through a numeric type).
        """
        if not value:
            return value

        digits = value.replace("-", "").replace(".", "").strip()

        if not digits.isdigit():
            raise ValueError("ZIP code must contain only digits.")
        if len(digits) not in (7, 8):
            raise ValueError("ZIP code must have 8 digits.")

        return digits.zfill(8)

    @field_validator("state_abbrev")
    @classmethod
    def validate_state_abbrev(cls, value: str):
        """Validate that the state abbreviation is valid (optional but must be 
        2 letters if provided)."""
        if value and len(value) != 2:
            raise ValueError("State abbreviation must be exactly 2 characters.")

        return value.upper() if value else value

    @model_validator(mode="before")
    @classmethod
    def clean_inputs(cls, values: dict):
        """Sanitize and validate inputs."""
        values["city_name"] = cls._remove_quotes(values.get("city_name", ""))
        values["cnae_code"] = cls._remove_quotes(values.get("cnae_code", ""))
        values["state_abbrev"] = cls._remove_quotes(values.get("state_abbrev", ""))
        values["zipcode"] = cls._remove_quotes(values.get("zipcode", ""))

        if values.get("only_mei") and values.get("unable_mei"):
            raise ValueError("Cannot filter for both MEI and non-MEI records.")

        return values

    @staticmethod
    def _remove_quotes(value: str) -> str:
        """Utility to remove quotes from string."""
        if value:
            return value.replace('"', "").replace("'", "")
        return value


class ModeloSimplesSimei(BaseModel):
    optante: bool = False
    data_opcao: Optional[str]
    data_exclusao: Optional[str]


class InvalidCNPJError(ValueError):
    pass


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

        self.basico_str = self._validate_digits(basico, 8, "basico")
        self.ordem_str = self._validate_digits(ordem, 4, "ordem")
        self.digitos_verificadores_str = self._validate_digits(
            digitos_verificadores, 2, "digitos_verificadores"
        )

    def _validate_digits(self, value: str, length: int, field_name: str) -> str:
        """Validate if the string contains numeric characters and has the expected length."""
        if not value.isdigit():
            raise InvalidCNPJError(
                f"Digits '{field_name}' contains non-numeric characters."
            )
        return value.zfill(length)

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
