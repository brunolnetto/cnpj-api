"""
Response schemas for the CNPJ endpoints.

They document the responses in OpenAPI without changing them:
- extra="allow": a field missing from a schema is passed through, not dropped;
- routes use response_model_exclude_unset=True, so fields absent from a
  response are not added as null;
- scalar fields accept null, so unexpected data does not turn into a 500.
"""

from typing import Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, ConfigDict, Field


class ResponseModel(BaseModel):
    model_config = ConfigDict(extra="allow")


class CodeText(ResponseModel):
    """A code from a reference table and its description."""

    code: str
    text: str


# Paginated listings return CodeText objects; with enable_pagination=false
# they return [code, CodeText] pairs
CodeTextListing = Union[List[CodeText], List[Tuple[str, CodeText]]]


class Activity(ResponseModel):
    """A CNAE activity. The code is a string, or an integer in the main
    activity of /cnpjs/{cnpj}/activities."""

    code: Union[str, int]
    text: str


class Activities(ResponseModel):
    atividade_principal: Activity
    atividades_secundarias: List[Activity]


class Partner(ResponseModel):
    nome: str = Field(..., description="Partner name")
    qual: str = Field(..., description="Qualification code and description")


class Partners(ResponseModel):
    qsa: List[Partner] = Field(..., description="Partners and administrators")


class TaxRegimeStatus(ResponseModel):
    optante: bool
    data_opcao: Optional[str] = Field(None, description="Opt-in date, dd/mm/yyyy")
    data_exclusao: Optional[str] = Field(None, description="Exit date, dd/mm/yyyy")


class SimplesSimei(ResponseModel):
    simples: TaxRegimeStatus
    simei: TaxRegimeStatus


class Company(ResponseModel):
    """The company (CNPJ base, first 8 digits)."""

    nome: Optional[str] = None
    porte: Optional[str] = None
    capital_social: Optional[str] = None
    natureza_juridica: Optional[str] = None
    efr: Optional[str] = Field(None, description="Responsible federative entity")


class Establishment(ResponseModel):
    """One establishment (headquarters or branch) of a company."""

    cnpj: Optional[str] = Field(None, description="Formatted CNPJ")
    tipo: Optional[str] = Field(None, description="MATRIZ or FILIAL")
    abertura: Optional[str] = None
    situacao: Optional[str] = None
    data_situacao: Optional[str] = None
    motivo_situacao: Optional[str] = None
    situacao_especial: Optional[str] = None
    data_situacao_especial: Optional[str] = None
    fantasia: Optional[str] = None
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    municipio: Optional[str] = None
    uf: Optional[str] = None
    cep: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    atividade_principal: Optional[Activity] = None
    atividades_secundarias: Optional[List[Activity]] = None


class CNPJRecord(Establishment, Company, Partners, SimplesSimei):
    """The full record of a CNPJ: establishment, company, partners and
    Simples/SIMEI."""

    cnpj_raw: str = Field(..., description="CNPJ with 14 digits, unformatted")


class CNPJValidation(ResponseModel):
    is_valid: bool
    reason: str


class CNPJBatchResult(ResponseModel):
    success: List[CNPJRecord]
    fail: Dict[str, CNPJValidation] = Field(
        ..., description="Invalid CNPJs of the batch and why"
    )


# Lookup tables served as {code: description}
CodeDescriptionMap = Dict[str, str]

# For each city name sent, the most similar known city names
CityCandidates = Dict[str, List[str]]
