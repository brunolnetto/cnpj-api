from typing import Tuple, Dict, Union, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from json import loads

import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.app.utils.misc import string_to_json
from backend.app.api.utils.cnpj import format_cnpj_list
from backend.app.api.utils.misc import paginate_dict
from backend.app.api.models.cnpj import CNPJ
from backend.app.api.repositories.cnpj import BaseRepository

from backend.app.utils.repositories import (
    format_database_date,
    format_cep,
    format_phone,
)
from backend.app.utils.misc import (
    replace_invalid_fields_on_list_tuple,
    replace_invalid_fields_on_list_dict,
    replace_spaces_on_list_tuple,
    format_decimal,
    replace_spaces,
    is_field_valid,
    is_number,
    number_string_to_number,
    humanize_string,
)
from backend.app.api.utils.cnpj import get_cnpj_code_description_entries
from backend.app.api.utils.misc import (
    zfill_factory,
    normalize_json,
    commify_list,
    comma_stringify_list,
)
from backend.app.api.utils.ml import find_most_possible_tokens
from backend.app.utils.dataframe import dataframe_to_nested_dict
from backend.app.api.utils.cnpj import format_cnpj
from backend.app.api.repositories.constants import (
    get_company_size_dict,
    get_company_situation_dict,
    get_establishment_type_dict,
)
from backend.app.database.base import get_session
from backend.app.setup.config import settings

# Types
CNPJList = List[CNPJ]
JSON = Dict[str, Any]
CodeType = Union[str, int]
CodeListType = List[CodeType]
PayloadType = Dict[str, str]


class CNPJRepository(BaseRepository):
    @classmethod
    def initialize_static_properties(cls, session: Session):
        cls.cnaes_dict = {
            str(cnae_info["code"]): cnae_info for cnae_info in cls.get_cnaes(session)
        }

        cls.legal_nature_dict = {
            str(legal_nature_info["code"]): legal_nature_info
            for legal_nature_info in cls.get_legal_natures(session)
        }

        cls.registration_statuses_dict = {
            str(registration_status_info["code"]): registration_status_info
            for registration_status_info in cls.get_registration_statuses(session)
        }

        cls.cities_dict = {
            str(city_info["code"]): city_info for city_info in cls.get_cities(session)
        }

        cls.company_size_dict = get_company_size_dict()
        cls.company_situation_dict = get_company_situation_dict()
        cls.establishment_type_dict = get_establishment_type_dict()

    @classmethod
    def initialize_on_startup(cls, session: Session):
        if not hasattr(cls, "cnaes_dict"):
            cls.initialize_static_properties(session)

    def get_cnpjs_raw(
        self,
        state_abbrev: str = "",
        city_code: str = "",
        cnae_code: str = "",
        zipcode: str = "",
        is_all: bool = False,
        limit: int = settings.PAGE_SIZE,
        offset: int = 0,
    ):
        """
        Get CNPJs on database according to (state_abbrev, city_code, cnae_code, zipcode).
        One may set filters is_all for checking all CNAE codes, limit for page size and
        offset for page start point.
        """
        # Filters
        state_condition = f"uf='{state_abbrev}'" if state_abbrev else "1=1"
        city_condition = f"municipio='{city_code}'" if city_code else "1=1"
        filled_zipcode = str(float(zipcode)) if zipcode else ""
        zipcode_condition = f"cep = '{filled_zipcode}'" if filled_zipcode else "1=1"

        if cnae_code:
            cnae_condition = (
                f"""(
            (
                cnae_fiscal_principal = '{cnae_code}' or
                cnae_fiscal_secundaria @> Array[{cnae_code}]
            ) and situacao_cadastral = '2'
        ) -- ATIVA"""
                if is_all
                else f"""(
            (
                cnae_fiscal_principal = '{cnae_code}'
            ) and situacao_cadastral = '2'
        ) -- ATIVA"""
            )
        else:
            cnae_condition = "1=1"

        query = text(
            f"""
                with estabelecimento_uf as (
                    select
                        concat(
                            lpad(cnpj_basico::text, 8, '0'),
                            lpad(cnpj_ordem::text, 4, '0'),
                            lpad(cnpj_dv::text, 2, '0')
                        ) as cnpj,
                        situacao_cadastral,
                        municipio,
                        uf,
                        cep,
                        cnae_fiscal_principal,
                        case
                            WHEN cnae_fiscal_secundaria = 'nan' THEN '{{}}'
                        else
                            string_to_array(cnae_fiscal_secundaria, ',')::INT[]
                        end as cnae_fiscal_secundaria
                    from estabelecimento
                    where {state_condition}
                ),
                estabelecimento_uf_cidade as (
                    select
                        *
                    from
                        estabelecimento_uf
                    where
                        {city_condition} and {zipcode_condition}
                )

                select cnpj
                from estabelecimento_uf_cidade
                where
                    {cnae_condition}
                limit
                    {limit}
                offset
                    {offset}
            """
        )

        cnpjs_result = replace_invalid_fields_on_list_tuple(
            self.session.execute(query).fetchall()
        )

        columns = ["cnpj"]
        cnpjs_df = pd.DataFrame(cnpjs_result, columns=columns)

        cnpjs_list = list(cnpjs_df["cnpj"])

        return cnpjs_list

    def is_code_key_valid(self, code_key: CodeType, code_dict: Dict[str, Any]) -> bool:
        """
        Validates a dict-related key

        Parameters:
        code_key (str): The dict code key.

        Returns:
        bool: a boolean value for CNAE validity.
        """
        return code_key and is_number(str(code_key)) and str(code_key) in code_dict

    def get_cnae(self, cnae_code: CodeType):
        """
        Get the CNAE for the code.

        Parameters:
        cnae_code (str): The code of the CNAE.

        Returns:
        str: The description of the CNAE.
        """
        return (
            {}
            if not self.is_code_key_valid(cnae_code, self.__class__.cnaes_dict)
            else self.cnaes_dict[str(cnae_code)]
        )

    def get_cnae_list(self, cnae_code_list: CodeListType):
        """
        Get the CNAE for the code.

        Parameters:
        cnae_code (str, int): The code of the CNAE.

        Returns:
        str: The description of the CNAE.
        """

        def is_cnaes_valid_map(cnae_code):
            return self.is_code_key_valid(cnae_code, self.__class__.cnaes_dict)

        return [
            self.get_cnae(cnae_code)
            for cnae_code in filter(is_cnaes_valid_map, cnae_code_list)
        ]

    def get_cnae_by_token(self, token: str):
        """
        Get the CNAE for the token.

        Parameters:
        token (str): The token to search for in the CNAE descriptions.

        Returns:
        list: A list of dictionaries with CNAE 'code' and 'text' fields.
        """
        # Ensure the token is not empty and handle it accordingly
        if not token:
            return []

        # Use parameterized queries to safely include the token in the query
        cnae_result = self.session.query(CNAE).filter(CNAE.descricao.ilike(f'%{token}%')).all()

        # Define a function to map the query results to a dictionary format
        def wrap_values_map(cnae):
            return {"code": cnae.id, "text": cnae.descricao}

        # Map the results to the desired format
        cnae_dict = [
            {"code": codigo, "text": descricao} for codigo, descricao in cnae_result
        ]

        return cnae_dict

    @staticmethod
    def get_cnaes(session):
        """
        Get all CNAEs from the database.

        Returns:
        DataFrame: The DataFrame with the CNAEs.
        """
        return get_cnpj_code_description_entries(session, "cnae")

    def get_paginated_cnaes(
        self,
        limit: int = settings.PAGE_SIZE,
        offset: int = 0,
        enable_pagination: bool = False,
    ):
        return (
            list(paginate_dict(self.__class__.cnaes_dict, limit, offset).values())
            if enable_pagination
            else list(self.__class__.cnaes_dict.items())
        )

    def get_legal_nature(self, legal_nature_code: CodeType):
        """
        Get legal nature from the database.

        Returns:
        dict: The dictionary with the legal nature code and text.
        """
        return (
            {}
            if not self.is_code_key_valid(legal_nature_code, self.legal_nature_dict)
            else self.legal_nature_dict[str(legal_nature_code)]
        )

    def get_legal_natures_list(self, legal_nature_list: CodeListType):
        """
        Get legal nature from the database.

        Returns:
        dict: The dictionary with the legal nature code and text.
        """

        def is_legal_nature_valid_map(legal_nature_code_):
            return self.is_code_key_valid(
                legal_nature_code_, self.__class__.legal_nature_dict
            )

        return [
            self.get_legal_nature(str(legal_nature_code))
            for legal_nature_code in filter(
                is_legal_nature_valid_map, legal_nature_list
            )
        ]

    @staticmethod
    def get_legal_natures(session):
        """
        Get all legal natures from the database.

        Returns:
        List: The List with the legal natures text and code.
        """
        return get_cnpj_code_description_entries(session, "natju")

    def get_paginated_legal_natures(
        self,
        limit: int = settings.PAGE_SIZE,
        offset: int = 0,
        enable_pagination: bool = False,
    ):
        return (
            list(
                paginate_dict(self.__class__.legal_nature_dict, limit, offset).values()
            )
            if enable_pagination
            else list(self.__class__.legal_nature_dict.items())
        )

    def get_registration_status_list(self, registration_status_list: CodeListType):
        """
        Get the reason for the signup situation.

        Parameters:
        code (str): The code of the signup situation.

        Returns:
        str: The reason for the signup situation.
        """

        def is_registration_status_valid_map(registration_status_code_):
            return self.is_code_key_valid(
                registration_status_code_, self.__class__.registration_statuses_dict
            )

        return [
            self.registration_statuses_dict[str(registration_status_code)]
            for registration_status_code in filter(
                is_registration_status_valid_map, registration_status_list
            )
        ]

    @staticmethod
    def get_registration_statuses(session):
        """
        Get all registration statuses from the database.

        Returns:
        List: The List with the registration statuses.
        """
        return get_cnpj_code_description_entries(session, "moti")

    def get_paginated_registration_statuses(
        self,
        limit: int = settings.PAGE_SIZE,
        offset: int = 0,
        enable_pagination: bool = False,
    ):
        """
        Get all registration statuses from the database.

        Returns:
        List: The List with the registration statuses.
        """
        return (
            list(
                paginate_dict(
                    self.__class__.registration_statuses_dict, limit, offset
                ).values()
            )
            if enable_pagination
            else list(self.__class__.registration_statuses_dict.items())
        )

    def city_exists(self, city_name: str):
        """
        Get the city for the code.

        Parameters:
        code (str): The code of the city.

        Returns:
        str: The name of the city.
        """
        if not city_name:
            return False, None

        query = text(
            f"""
                select
                    codigo, descricao
                from
                    munic
                where
                    descricao = '{city_name}'
            """
        )

        city_result = self.session.execute(query).fetchall()

        columns = ["code", "text"]
        empty_df = pd.DataFrame(columns=columns)
        city_df = (
            empty_df
            if len(city_result) == 0
            else pd.DataFrame(city_result, columns=columns)
        )
        city_obj = (
            city_df.to_dict()
            if len(city_result) == 0
            else city_df.to_dict(orient="records")[0]
        )
        has_city = len(city_result) != 0

        return has_city, city_obj if has_city else None

    def get_city(self, city_code: str):
        """
        Get the city for the code.

        Parameters:
        code (str): The code of the city.

        Returns:
        str: The name of the city.
        """
        return (
            {}
            if not self.is_code_key_valid(city_code, self.__class__.cities_dict)
            else self.cities_dict[city_code]
        )

    @staticmethod
    def get_cities(session):
        """
        Get the city for the code.

        Parameters:
        code (str): The code of the city.

        Returns:
        str: The name of the city.
        """
        return get_cnpj_code_description_entries(session, "munic")

    def get_paginated_cities(self, limit: int = settings.PAGE_SIZE, offset: int = 0):
        return list(paginate_dict(self.__class__.cities_dict, limit, offset).values())

    def get_city_candidates(self, city_candidates_list: CodeListType):
        """
        Get the city for the code.

        Parameters:
        code (str): The code of the city.

        Returns:
        str: The name of the city.
        """
        city_candidates_list = list(set(city_candidates_list))
        lower_city_candidates_list = [
            city_candidate.lower() for city_candidate in city_candidates_list
        ]
        elegible_cities_text = [
            city_dict["text"] for city_dict in self.cities_dict.values()
        ]

        # NOTE: Hard coded limit_count = 3
        LIMIT_COUNT = 3

        return {
            city_candidate: find_most_possible_tokens(
                elegible_cities_text, lower_city_candidate, LIMIT_COUNT
            )
            for lower_city_candidate, city_candidate in zip(
                lower_city_candidates_list, city_candidates_list
            )
        }

    def get_cities_list(self, cities_code_list: CodeListType):
        """
        Get the list of city object by the code.

        Parameters:
        code (CodeListType): The code of the city.

        Returns:
        List[dict]: The name of the city.
        """

        def is_city_valid_map(city_code_):
            return self.is_code_key_valid(city_code_, self.__class__.cities_dict)

        return [
            self.cities_dict[str(city_code)]
            for city_code in filter(is_city_valid_map, cities_code_list)
        ]

    def __format_company(self, company_dict: Dict[str, Any]):
        company_dict["capital_social"] = format_decimal(company_dict["capital_social"])
        company_dict["porte"] = self.company_size_dict[
            str(number_string_to_number(company_dict["porte_empresa"]))
        ]
        del company_dict["porte_empresa"]

        return company_dict

    def get_cnpjs_company(self, cnpj_list: CNPJList):
        """
        Get the company for the CNPJ.

        Parameters:
        cnpj (CNPJ): The CNPJ object.

        Returns:
        DataFrame: The DataFrame with the company.
        """
        cnpj_basicos_str = comma_stringify_list([cnpj.basico_int for cnpj in cnpj_list])

        columns = [
            "cnpj_basico",
            "razao_social",
            "ente_federativo_responsavel",
            "porte_empresa",
            "capital_social",
            "natureza_juridica",
        ]
        columns_str = commify_list(columns)

        query = text(
            f"""
            with empresa_ as (
                select
                    {columns_str}
                from empresa emp
                    where emp.cnpj_basico in ({cnpj_basicos_str})
            )
            select
                distinct on (cnpj_basico)
                cnpj_basico,
                razao_social,
                ente_federativo_responsavel,
                porte_empresa,
                capital_social,
                concat(natju.codigo, '-', natju.descricao) as natureza_juridica
            from
                empresa_ emp
            left join natju on natju.codigo::text = emp.natureza_juridica::text
            """
        )

        with get_session(settings.POSTGRES_DBNAME_RFB) as session:
            company_result = session.execute(query).fetchall()

        company_result = replace_invalid_fields_on_list_tuple(company_result)
        company_result = replace_spaces_on_list_tuple(company_result)

        empty_df = pd.DataFrame(columns=columns)
        company_df = pd.DataFrame(company_result, columns=columns)
        company_df = empty_df if len(company_result) == 0 else company_df
        company_df["cnpj_basico"] = company_df["cnpj_basico"].apply(zfill_factory(8))

        if len(company_df) == 0:
            return []

        company_dict = dataframe_to_nested_dict(company_df, "cnpj_basico")

        def item_map(item):
            return item[0], self.__format_company(item[1])

        company_dict = dict(map(item_map, company_dict.items()))

        cnpjs_base = [cnpj.to_tuple()[0] for cnpj in cnpj_list]

        companies_dict = {
            cnpj.to_raw(): company_dict[cnpj_base]
            for cnpj_base, cnpj in zip(cnpjs_base, cnpj_list)
            if cnpj_base in company_dict
        }

        return companies_dict

    def __format_establishment(self, establishment_dict: Dict[str, Any]):
        """
        Formats the establishment dictionary.

        Args:
            establishment_dict (Dict): The establishment dictionary to format.

        Returns:
            Dict: The formatted establishment dictionary.
        """
        data_inicio_atividade = establishment_dict["data_inicio_atividade"]
        establishment_dict["abertura"] = format_database_date(data_inicio_atividade)
        del establishment_dict["data_inicio_atividade"]

        establishment_dict["email"] = establishment_dict["correio_eletronico"].lower()
        del establishment_dict["correio_eletronico"]

        basico = establishment_dict["cnpj_basico"].zfill(8)
        ordem = establishment_dict["cnpj_ordem"].zfill(4)
        dv = establishment_dict["cnpj_dv"].zfill(2)
        establishment_dict["cnpj"] = format_cnpj(f"{basico}{ordem}{dv}")

        del establishment_dict["cnpj_basico"]
        del establishment_dict["cnpj_ordem"]
        del establishment_dict["cnpj_dv"]

        # Get the registration status
        registration_status = establishment_dict["situacao_cadastral"]
        situacao_cadastral = str(number_string_to_number(registration_status))

        establishment_dict["situacao"] = self.company_situation_dict[situacao_cadastral]
        del establishment_dict["situacao_cadastral"]

        establishment_dict["fantasia"] = humanize_string(
            establishment_dict["nome_fantasia"]
        )
        del establishment_dict["nome_fantasia"]

        data_situacao_cadastral = establishment_dict["data_situacao_cadastral"]
        establishment_dict["data_situacao"] = format_database_date(
            data_situacao_cadastral
        )
        del establishment_dict["data_situacao_cadastral"]

        registration_reason = establishment_dict["motivo_situacao_cadastral"]
        establishment_dict["motivo_situacao"] = registration_reason

        del establishment_dict["motivo_situacao_cadastral"]

        # Format the phone number

        # Check if the DDD columns are invalid
        ddd_1 = establishment_dict["ddd_1"]
        ddd_2 = establishment_dict["ddd_2"]
        telefone_1 = establishment_dict["telefone_1"]
        telefone_2 = establishment_dict["telefone_2"]

        # Format the phone number
        is_1_invalid = is_field_valid(ddd_1)
        is_2_invalid = is_field_valid(ddd_2)

        telefone_1 = "" if is_1_invalid else format_phone(ddd_1, telefone_1)
        telefone_2 = "" if is_2_invalid else format_phone(ddd_2, telefone_2)
        delimiter = " / " if telefone_1 and telefone_1 else ""

        establishment_dict["telefone"] = telefone_1 + delimiter + telefone_2

        del establishment_dict["ddd_1"]
        del establishment_dict["telefone_1"]
        del establishment_dict["ddd_2"]
        del establishment_dict["telefone_2"]

        # Format address
        address_type = establishment_dict["tipo_logradouro"]
        address_name = establishment_dict["logradouro"]
        address_type = replace_spaces(address_type).strip()
        address_name = replace_spaces(address_name).strip()
        address = humanize_string(address_type + " " + address_name)

        establishment_dict["logradouro"] = address
        del establishment_dict["tipo_logradouro"]

        # Format UF
        complement = establishment_dict["complemento"]
        establishment_dict["complemento"] = humanize_string(complement)
        establishment_dict["bairro"] = humanize_string(establishment_dict["bairro"])

        # Format CEP
        zip_code = establishment_dict["cep"]
        establishment_dict["cep"] = format_cep(zip_code)

        # Get the company type
        identificador = establishment_dict["identificador_matriz_filial"]
        establishment_dict["tipo"] = self.establishment_type_dict[identificador]

        del establishment_dict["identificador_matriz_filial"]

        # Get city name
        city_code = establishment_dict["municipio"]
        city_dict = self.get_city(city_code)
        city_label = city_dict["text"]

        establishment_dict["municipio"] = humanize_string(city_label)

        # Get the main CNAE
        atividade_principal = establishment_dict["cnae_fiscal_principal"]

        establishment_dict["atividade_principal"] = (
            self.get_cnae(atividade_principal) if atividade_principal else {}
        )

        del establishment_dict["cnae_fiscal_principal"]

        # Get the secondary CNAEs
        side_activities_str = establishment_dict["cnae_fiscal_secundaria"]

        if is_field_valid(side_activities_str):
            cnae_list = side_activities_str.split(",")
            has_side_cnaes = len(cnae_list) != 0 and cnae_list[0] != ""

            side_activity_names = []
            if has_side_cnaes:
                cnae_list = [str(int(cnae_str.strip())) for cnae_str in cnae_list]
                side_activity_names = self.get_cnae_list(cnae_list)

            establishment_dict["atividades_secundarias"] = side_activity_names
        else:
            establishment_dict["atividades_secundarias"] = []

        del establishment_dict["cnae_fiscal_secundaria"]

        list_dict = [establishment_dict]
        list_dict = replace_invalid_fields_on_list_dict(list_dict)
        establishment_dict = list_dict[0]

        return establishment_dict

    def get_cnpjs_establishment(self, cnpj_list: CNPJList) -> Dict:
        columns = [
            "cnpj_basico",
            "cnpj_ordem",
            "cnpj_dv",
            "correio_eletronico",
            "data_inicio_atividade",
            "data_situacao_cadastral",
            "situacao_cadastral",
            "motivo_situacao_cadastral",
            "nome_fantasia",
            "tipo_logradouro",
            "logradouro",
            "numero",
            "complemento",
            "bairro",
            "municipio",
            "cep",
            "uf",
            "cnae_fiscal_principal",
            "cnae_fiscal_secundaria",
            "identificador_matriz_filial",
            "situacao_especial",
            "data_situacao_especial",
            "ddd_1",
            "telefone_1",
            "ddd_2",
            "telefone_2",
        ]
        columns_str = commify_list(columns)

        cnpjs_basicos_str = comma_stringify_list(
            [cnpj.basico_int for cnpj in cnpj_list]
        )
        cnpjs_ordem_str = comma_stringify_list([cnpj.ordem_int for cnpj in cnpj_list])
        cnpjs_dv_str = comma_stringify_list(
            [cnpj.digitos_verificadores_int for cnpj in cnpj_list]
        )

        # Create the table if it does not exist
        query = text(
            f"""
                select
                    {columns_str}
                from
                    estabelecimento est
                where
                    est.cnpj_basico in ({cnpjs_basicos_str}) AND
                    est.cnpj_ordem in ({cnpjs_ordem_str}) AND
                    est.cnpj_dv in ({cnpjs_dv_str})
            """
        )

        with get_session(settings.POSTGRES_DBNAME_RFB) as session:
            establishment_result = session.execute(query).fetchall()

        empty_df = pd.DataFrame(columns=columns)
        df_is_empty = len(establishment_result) == 0
        if df_is_empty:
            return {}

        establishment_result = replace_invalid_fields_on_list_tuple(
            establishment_result
        )
        establishment_result = replace_spaces_on_list_tuple(establishment_result)

        establishment_df = pd.DataFrame(establishment_result, columns=columns)
        establishment_df = (
            empty_df if len(establishment_result) == 0 else establishment_df
        )

        registration_status = establishment_df["motivo_situacao_cadastral"]
        registration_status = registration_status.map(self.registration_statuses_dict)
        establishment_df["motivo_situacao_cadastral"] = registration_status

        cnpj_base_series = establishment_df["cnpj_basico"]
        cnpj_ordem_series = establishment_df["cnpj_ordem"]
        cnpj_dv_series = establishment_df["cnpj_dv"]

        establishment_df["cnpj_"] = (
            cnpj_base_series.apply(zfill_factory(8))
            + cnpj_ordem_series.apply(zfill_factory(4))
            + cnpj_dv_series.apply(zfill_factory(2))
        )
        establishment_dict = dataframe_to_nested_dict(establishment_df, "cnpj_")

        def item_map(item):
            return item[0], self.__format_establishment(item[1])

        establishment_dict = dict(map(item_map, establishment_dict.items()))

        return establishment_dict

    def get_cnpj_establishments(self, cnpj: CNPJ) -> List:
        columns = [
            "cnpj_basico",
            "cnpj_ordem",
            "cnpj_dv",
            "correio_eletronico",
            "data_inicio_atividade",
            "data_situacao_cadastral",
            "situacao_cadastral",
            "motivo_situacao_cadastral",
            "nome_fantasia",
            "tipo_logradouro",
            "logradouro",
            "numero",
            "complemento",
            "bairro",
            "municipio",
            "cep",
            "uf",
            "cnae_fiscal_principal",
            "cnae_fiscal_secundaria",
            "identificador_matriz_filial",
            "situacao_especial",
            "data_situacao_especial",
            "ddd_1",
            "telefone_1",
            "ddd_2",
            "telefone_2",
        ]

        # Create the table if it does not exist
        establishment_colums_str = commify_list(columns)
        query = text(
            f"""
                select distinct {establishment_colums_str}
                from estabelecimento est
                where est.cnpj_basico = '{cnpj.basico_int}'
                order by 1, 2
            """
        )

        with get_session(settings.POSTGRES_DBNAME_RFB) as session:
            establishment_result = session.execute(query)
            establishment_result = establishment_result.fetchall()

        establishment_result = replace_invalid_fields_on_list_tuple(
            establishment_result
        )
        establishment_result = replace_spaces_on_list_tuple(establishment_result)

        empty_df = pd.DataFrame(columns=columns)
        establishment_df = pd.DataFrame(establishment_result, columns=columns)
        establishment_df = (
            empty_df if len(establishment_result) == 0 else establishment_df
        )

        establishment_df["cnpj_ordem"] = establishment_df["cnpj_ordem"].apply(int)
        establishment_df = establishment_df.sort_values(by=["cnpj_ordem"])
        establishment_df["cnpj_ordem"] = establishment_df["cnpj_ordem"].apply(str)

        establishment_list = establishment_df.to_dict(orient="records")

        est_is_empty = len(establishment_df) == 0
        format_map = self.__format_establishment

        return [] if est_is_empty else list(map(format_map, establishment_list))

    def get_cnpjs_partners(self, cnpj_list: CNPJList) -> List:
        """
        Get the partners for the CNPJ.

        Parameters:
        cnpj (CNPJ): The CNPJ object.

        Returns:
        DataFrame: The DataFrame with the partners.
        """
        cnpj_basicos_str = format_cnpj_list(cnpj_list)

        query = text(
            f"""
                with socios_ as (
                    select
                        cnpj_basico,
                        qualificacao_socio,
                        nome_socio_razao_social
                    from
                        socios
                    where
                        cnpj_basico IN ({cnpj_basicos_str})
                    group by
                        1, 2, 3
                )
                SELECT
                    cnpj_basico,
                    json_agg(
                        json_build_object(
                            'nome', nome_socio_razao_social,
                            'qual', concat(qualificacao_socio,'-', qual_socio.descricao)
                        )
                    ) AS qsa
                FROM
                    socios_ soc
                left join
                    quals qual_socio
                on
                    qual_socio.codigo::text = soc.qualificacao_socio::text
                GROUP BY
                    cnpj_basico
            """
        )

        with get_session(settings.POSTGRES_DBNAME_RFB) as session:
            partners_result = session.execute(query)
            partners_result = partners_result.fetchall()

        partners_result = replace_invalid_fields_on_list_tuple(partners_result)
        partners_result = replace_spaces_on_list_tuple(partners_result)

        columns = ["cnpj_basico", "qsa"]
        empty_df = pd.DataFrame(columns=columns)

        partners_df = pd.DataFrame(partners_result, columns=columns)
        partners_df = empty_df if len(partners_df) == 0 else partners_df

        partners_df["qsa"] = partners_df["qsa"].apply(string_to_json)
        partners_df["cnpj_basico"] = partners_df["cnpj_basico"].apply(zfill_factory(8))
        partners_dict = dataframe_to_nested_dict(partners_df, index_col="cnpj_basico")

        cnpjs_raw_base = [(cnpj.to_raw(), cnpj.to_tuple()[0]) for cnpj in cnpj_list]

        empty_dict = {"qsa": []}

        def cnpj_map(cnpj_base_):
            return (
                partners_dict[cnpj_base_] if cnpj_base_ in partners_dict else empty_dict
            )

        partners_dict = {
            cnpj_raw: cnpj_map(cnpj_base)
            for cnpj_raw, cnpj_base in cnpjs_raw_base
            if cnpj_base in partners_dict
        }

        return partners_dict

    def parse_simples_simei(
        self, payload: PayloadType
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Parse the payload to ensure correct data types.

        :param payload: Dictionary with 'optante', 'data_opcao', and 'data_exclusao' keys.
        :return: Tuple with boolean, and optional strings for dates.
        """

        # Convert 'optante' to boolean
        optante_str = payload.get("optante", "false").lower()
        optante = optante_str in ["true", "1"]

        # Extract and validate dates
        data_opcao = payload.get("data_opcao")
        data_exclusao = payload.get("data_exclusao")

        # Handle 'null' as None
        if data_opcao == "null":
            data_opcao = None
        if data_exclusao == "null":
            data_exclusao = None

        return (optante, data_opcao, data_exclusao)

    def get_cnpjs_simples_simei(self, cnpj_list: CNPJList) -> List:
        """
        Get the partners for the CNPJ.

        Parameters:
        cnpj (CNPJ): The CNPJ object.

        Returns:
        DataFrame: The DataFrame with the partners.
        """
        cnpj_basicos_str = comma_stringify_list([cnpj.basico_int for cnpj in cnpj_list])

        query = text(
            f"""
            SELECT
                cnpj_basico,
                json_build_object(
                    'optante',
                    case when opcao_pelo_simples ilike 'S' then 'true' else 'false' end,
                    'data_opcao', COALESCE(
                        TO_CHAR(
                            TO_DATE(
                                NULLIF(data_opcao_simples, '0'),  -- Replace '0' with NULL
                                'YYYYMMDD'
                            ),
                            'DD/MM/YYYY'
                        ),
                        'null'  -- Default value if the date is invalid or NULL
                    ),
                    'data_exclusao', COALESCE(
                        TO_CHAR(
                            TO_DATE(
                                NULLIF(data_exclusao_simples, '0'),  -- Replace '0' with NULL
                                'YYYYMMDD'
                            ),
                            'DD/MM/YYYY'
                        ),
                        'null'  -- Default value if the date is invalid or NULL
                    )
                ) AS simples,
                json_build_object(
                    'optante', case when opcao_mei ilike 'S' then 'true' else 'false' end,
                    'data_opcao', COALESCE(
                        TO_CHAR(
                            TO_DATE(
                                NULLIF(data_opcao_mei, '0'),  -- Replace '0' with NULL
                                'YYYYMMDD'
                            ),
                            'DD/MM/YYYY'
                        ),
                        'null'  -- Default value if the date is invalid or NULL
                    ),
                    'data_exclusao', COALESCE(
                        TO_CHAR(
                            TO_DATE(
                                NULLIF(data_exclusao_mei, '0'),
                                'YYYYMMDD'
                            ),
                            'DD/MM/YYYY'
                        ),
                        'null'
                    )
                ) AS simei
            FROM
                simples soc
                where
                    cnpj_basico IN ({cnpj_basicos_str})
            """
        )

        with get_session(settings.POSTGRES_DBNAME_RFB) as session:
            simples_simei_result = session.execute(query)

        simples_simei_result = simples_simei_result.fetchall()
        simples_simei_result = replace_invalid_fields_on_list_tuple(
            simples_simei_result
        )
        simples_simei_result = replace_spaces_on_list_tuple(simples_simei_result)

        columns = ["cnpj_basico", "simples", "simei"]
        pd.DataFrame(columns=columns)

        simples_simei_df = pd.DataFrame(simples_simei_result, columns=columns)
        simples_simei_df = (
            simples_simei_df if len(simples_simei_df) == 0 else simples_simei_df
        )

        simples_simei_df["cnpj_basico"] = simples_simei_df["cnpj_basico"].apply(
            zfill_factory(8)
        )

        cnpjs_raw_base = [(cnpj.to_raw(), cnpj.to_tuple()[0]) for cnpj in cnpj_list]

        not_selected_dict = {
            "optante": False,
            "data_opcao": None,
            "data_exclusao": None,
        }
        empty_dict = {"simples": not_selected_dict, "simei": not_selected_dict}

        simples_simei_dict = dataframe_to_nested_dict(
            simples_simei_df, index_col="cnpj_basico"
        )

        def cnpj_map(cnpj_base_):
            simples_str = simples_simei_dict.get(cnpj_base_, {}).get("simples", "{}")
            normalized_json = normalize_json(simples_str)
            simples_dict = loads(normalized_json)

            simei_str = simples_simei_dict.get(cnpj_base_, {}).get("simei", "{}")
            normalized_json = normalize_json(simei_str)
            simei_dict = loads(normalized_json)

            return (
                {
                    "simples": (
                        dict(
                            zip(
                                ["optante", "data_opcao", "data_exclusao"],
                                self.parse_simples_simei(simples_dict),
                            )
                        )
                        if simples_dict["optante"]
                        else not_selected_dict
                    ),
                    "simei": (
                        dict(
                            zip(
                                ["optante", "data_opcao", "data_exclusao"],
                                self.parse_simples_simei(simei_dict),
                            )
                        )
                        if simei_dict["optante"]
                        else not_selected_dict
                    ),
                }
                if cnpj_base_ in simples_simei_dict
                else empty_dict
            )

        simples_simei_dict = {
            cnpj_raw: cnpj_map(cnpj_base) for cnpj_raw, cnpj_base in cnpjs_raw_base
        }

        return simples_simei_dict

    def get_cnpj_activities(self, cnpj: CNPJ):
        """
        Get the activities for the CNPJ.

        Parameters:
        cnpj (CNPJ): The CNPJ object.

        Returns:
        DataFrame: The DataFrame with the activities.
        """
        query = text(
            f"""
                with cnae_unnest as (
                    select
                        cnpj_basico,
                        unnest(
                            string_to_array(
                                est.cnae_fiscal_secundaria, ','
                            )
                        )::integer AS codigo_cnae
                    FROM estabelecimento est
                    where cnpj_basico::text = '{cnpj.basico_int}'
                ),
                nosso_cnae as (
                    select
                        cnpj_basico,
                        codigo,
                        descricao
                    from
                        cnae_unnest
                    inner join
                        cnae
                    on cnae.codigo::text = cnae_unnest.codigo_cnae::text
                    group by cnpj_basico, codigo, descricao
                    order by cnpj_basico, codigo, descricao
                ),
                atividade_principal as (
                    select
                        cnpj_basico,
                        json_build_object(
                            'code', cnae.codigo::integer,
                            'text', cnae.descricao
                        ) as atividade_principal
                    from estabelecimento est
                    inner join cnae
                        on est.cnae_fiscal_principal::text = cnae.codigo::text
                    where cnpj_basico::text = '{cnpj.basico_int}'
                ),
                atividades_secundarias as (
                    select
                        cnpj_basico,
                        json_agg(
                            json_build_object(
                                'code', codigo,
                                'text', descricao
                            )
                        ) as atividades_secundarias
                    from nosso_cnae
                    group by cnpj_basico
                )
                select
                    a_s.cnpj_basico as cnpj_basico,
                    a_p.atividade_principal as atividade_principal,
                    a_s.atividades_secundarias as atividades_secundarias
                from
                    atividades_secundarias a_s
                inner join
                    atividade_principal a_p
                on
                    a_s.cnpj_basico::text = a_p.cnpj_basico::text
            """
        )

        with get_session(settings.POSTGRES_DBNAME_RFB) as session:
            activities_result = session.execute(query).fetchall()

        activities_result = replace_invalid_fields_on_list_tuple(activities_result)
        activities_result = replace_spaces_on_list_tuple(activities_result)

        columns = ["cnpj_basico", "atividade_principal", "atividades_secundarias"]
        partners_df = pd.DataFrame(activities_result, columns=columns)
        empty_df = pd.DataFrame(columns=columns)

        partners_df = empty_df if len(partners_df) == 0 else partners_df

        partners_dict = partners_df.to_dict(orient="records")[0]

        main_activities_str = partners_dict["atividade_principal"]
        side_activities_str = partners_dict["atividades_secundarias"]
        main_activities = string_to_json(main_activities_str)
        side_activities = string_to_json(side_activities_str)

        is_empty = len(side_activities) == 1 and side_activities[0] == {}
        side_activities = [] if is_empty else side_activities

        return {
            "atividade_principal": main_activities,
            "atividades_secundarias": side_activities,
        }

    def get_cnpjs_info(self, cnpj_list: CNPJList) -> JSON:
        """
        Get the information for the CNPJ.

        Parameters:
        cnpj (CNPJ): The CNPJ object.

        Returns:
        dict: The dictionary with the CNPJ information.
        """
        columns = [
            "cnpj",
            "cnpj_raw",
            "abertura",
            "tipo",
            "nome",
            "fantasia",
            "capital_social",
            "porte",
            "logradouro",
            "numero",
            "complemento",
            "bairro",
            "municipio",
            "uf",
            "cep",
            "email",
            "telefone",
            "situacao",
            "data_situacao",
            "motivo_situacao",
            "situacao_especial",
            "data_situacao_especial",
            "atividade_principal",
            "atividades_secundarias",
            "efr",
            "qsa",
            "simples",
            "simei",
        ]

        # Define the methods to run in parallel
        tasks = {
            "establishment": self.get_cnpjs_establishment,
            "company": self.get_cnpjs_company,
            "partners": self.get_cnpjs_partners,
            "simples_simei": self.get_cnpjs_simples_simei,
        }

        results = {}

        # Run the tasks in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            # Create a future for each task
            future_to_task = {
                executor.submit(task, cnpj_list): name for name, task in tasks.items()
            }

            # Collect the results as they complete
            for future in as_completed(future_to_task):
                task_name = future_to_task[future]
                try:
                    results[task_name] = future.result()
                except Exception as e:
                    results[task_name] = f"Error occurred: {e}"

        # Combine all the results into a single dictionary and return it
        establishment_dict = results.get("establishment", {})
        company_dict = results.get("company", {})
        partners_dict = results.get("partners", {})
        simples_simei_dict = results.get("simples_simei", {})

        establ_set = set(establishment_dict)
        companies_set = set(company_dict)
        partners_set = set(partners_dict)
        simples_simei_set = set(simples_simei_dict)

        # XXX: Review missing information on original methods
        common_keys = list(
            establ_set.intersection(companies_set)
            .intersection(partners_set)
            .intersection(simples_simei_set)
        )

        cnpj_info_dict = {
            common_key: {
                **establishment_dict[common_key],
                **company_dict[common_key],
                **partners_dict[common_key],
                **simples_simei_dict[common_key],
            }
            for common_key in common_keys
        }

        # XXX: Fix scrap according to new route structure
        # cnpj_scrap_service=get_cnpj_scrap_service()
        # update_at = cnpj_scrap_service.max_update_at()

        cnpj_infos = {
            cnpj_key: {
                "cnpj_raw": cnpj_key,
                # "ultima_atualizacao": update_at.strftime(date_format),
                **cnpj_info,
            }
            for cnpj_key, cnpj_info in cnpj_info_dict.items()
        }

        print(cnpj_infos)

        return [
            {key_: cnpj_infos[key][key_] for key_ in columns if key_ in cnpj_infos[key]}
            for key in cnpj_infos
        ]

    def get_cnpj_info(self, cnpj: CNPJ) -> JSON:
        """
        Get the information for the CNPJ.

        Parameters:
        cnpj (CNPJ): The CNPJ object.

        Returns:
        dict: The dictionary with the CNPJ information.
        """
        columns = [
            "cnpj_raw",
            "cnpj",
            "abertura",
            "situacao",
            "data_situacao",
            "motivo_situacao",
            "situacao_especial",
            "data_situacao_especial",
            "tipo",
            "nome",
            "fantasia",
            "porte",
            "natureza_juridica",
            "capital_social",
            "atividade_principal",
            "atividades_secundarias",
            "logradouro",
            "numero",
            "complemento",
            "municipio",
            "bairro",
            "uf",
            "cep",
            "email",
            "telefone",
            "efr",
            "qsa",
        ]
        pd.DataFrame(columns=columns)

        cnpj_info = self.get_cnpjs_info([cnpj])[0]

        return cnpj_info if len(cnpj_info) != 0 else []

    def get_cnpjs_with_cnae(
        self, cnae_code: str, limit: int = settings.PAGE_SIZE, offset: int = 0
    ):
        """
        Get the companies with the CNAE.

        Parameters:
        cnae_code (str): The code of the CNAE.

        Returns:
        DataFrame: The DataFrame with the companies.
        """
        query = text(
            f"""
                select
                    distinct on (cnpj_basico)
                    cnpj_basico, cnpj_ordem, cnpj_dv
                from
                    estabelecimento
                where
                    (
                        cnae_fiscal_principal = '{cnae_code}' or
                        cnae_fiscal_secundaria like '%{cnae_code}%'
                    ) and
                    situacao_cadastral = '2' -- ATIVA
                order by
                    1, 2
                limit
                    {limit}
                offset
                    {offset}
            """
        )

        result = self.session.execute(query)
        cnpj_tuples = result.fetchall()

        cnpjs_str_list = [
            CNPJ(cnpj_base, cnpj_order, cnpj_digits)
            for cnpj_base, cnpj_order, cnpj_digits in cnpj_tuples
        ]

        return self.get_cnpjs_info(cnpjs_str_list)

    def get_cnpjs_by_cnaes(
        self, cnaes_list: CodeListType, limit: int = settings.PAGE_SIZE, offset: int = 0
    ):
        """
        Get the companies by the CNAEs.

        Parameters:
        cnaes_list (CodeListType): The list of CNAEs.

        Returns:
        Dict: The dictionary with the CNPJs info.
        """
        cnaes_str = comma_stringify_list(cnaes_list)

        main_cnae_str_condition = f"cnae_fiscal_principal in ({cnaes_str})"
        side_cnae_str_condition = " or ".join(
            [f"cnae_fiscal_secundaria like '%{cnae}%'" for cnae in cnaes_list]
        )

        query = text(
            f"""
                select
                    distinct on (cnpj_basico)
                    cnpj_basico, cnpj_ordem, cnpj_dv
                from
                    estabelecimento
                where
                    (
                        {main_cnae_str_condition} or
                        {side_cnae_str_condition}
                    ) and
                    situacao_cadastral::text = '2' -- ATIVA
                order by
                    1, 2
                limit
                    {limit}
                offset
                    {offset}
            """
        )

        result = self.session.execute(query)
        cnpj_tuples = result.fetchall()

        cnpjs_str_list = [
            CNPJ(cnpj_base, cnpj_order, cnpj_digits)
            for cnpj_base, cnpj_order, cnpj_digits in cnpj_tuples
        ]

        return self.get_cnpjs_info(cnpjs_str_list)

    def get_cnpjs_by_states(
        self,
        states_list: CodeListType,
        limit: int = settings.PAGE_SIZE,
        offset: int = 0,
    ):
        """
        Get the companies by the states.

        Parameters:

        Returns:
        Dict: The dictionary with the CNPJs info.
        """

        states_str = comma_stringify_list(states_list)

        query = text(
            f"""
                select
                    distinct on (cnpj_basico)
                    cnpj_basico, cnpj_ordem, cnpj_dv
                from
                    estabelecimento
                where
                    uf in ({states_str}) and
                    situacao_cadastral::text = '2' -- ATIVA
                order by
                    1, 2
                limit
                    {limit}
                offset
                    {offset}
            """
        )

        result = self.session.execute(query)
        cnpj_tuples = result.fetchall()

        cnpjs_str_list = [
            CNPJ(cnpj_base, cnpj_order, cnpj_digits)
            for cnpj_base, cnpj_order, cnpj_digits in cnpj_tuples
        ]

        return self.get_cnpjs_info(cnpjs_str_list)
