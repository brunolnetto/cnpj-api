from typing import Dict, Union, List, Any
from sqlalchemy import text
import pandas as pd
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.utils.misc import string_to_json
from backend.app.api.models.cnpj import CNPJ
from backend.app.api.services.scrapper import get_cnpj_scrap_service
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
from backend.app.api.utils.ml import find_most_possible_tokens
from backend.app.utils.dataframe import dataframe_to_nested_dict
from backend.app.api.utils.cnpj import format_cnpj
from backend.app.api.repositories.constants import (
    SIZE_DICT,
    SITUATION_DICT,
    EST_TYPE_DICT,
)


# Types
CNPJList = List[CNPJ]
JSON = Dict[str, Any]
CodeType = Union[str, int]
CodeListType = List[CodeType]


class CNPJRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def get_cnpjs_raw(
        self,
        state_abbrev: str = "",
        city_code: str = "",
        cnae_code: str = "",
        zipcode: str = "",
        is_all: bool = False,
        limit: int = 10,
        offset: int = 0,
    ):
        """
        Get all CNPJs from the database.

        Returns:
        DataFrame: The DataFrame with the CNPJs.
        """
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
        cnpjs_result = self.session.execute(query)
        cnpjs_result = cnpjs_result.fetchall()

        cnpjs_result = replace_invalid_fields_on_list_tuple(cnpjs_result)

        columns = ["cnpj"]
        cnpjs_df = pd.DataFrame(cnpjs_result, columns=columns)

        cnpjs_list = list(cnpjs_df["cnpj"])

        return cnpjs_list

    def get_cnae(self, cnae_code: CodeType):
        """
        Get the CNAE for the code.

        Parameters:
        cnae_code (str): The code of the CNAE.

        Returns:
        str: The description of the CNAE.
        """
        if not cnae_code and not is_number(cnae_code):
            return {}

        query = text(
            f"""
            select
                descricao
            from
                cnae
            where
                codigo::text = '{cnae_code}'
        """
        )

        cnae_result = self.session.execute(query).fetchall()

        cnae_description = "" if len(cnae_result) == 0 else cnae_result[0][0]

        return (
            {}
            if len(cnae_description) == 0
            else {
                "code": int(cnae_code),
                "text": cnae_description,
            }
        )

    def get_cnae_list(self, cnae_code_list: CodeListType):
        """
        Get the CNAE for the code.

        Parameters:
        cnae_code (str, int): The code of the CNAE.

        Returns:
        str: The description of the CNAE.
        """
        cnae_code_str = ",".join(
            [f"'{str(cnae_code)}'" for cnae_code in cnae_code_list]
        )

        query = text(
            f"""
            select
                distinct
                codigo,
                descricao
            from
                cnae
            where
                codigo::text in ({cnae_code_str})
        """
        )

        cnae_result = self.session.execute(query).fetchall()

        def wrap_values_map(code_text):
            return {"code": code_text[0], "text": code_text[1]}

        cnae_dict = list(map(wrap_values_map, cnae_result))

        return cnae_dict

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
        cnae_result = (
            self.session.execute(
                text(
                    f"select codigo, descricao from cnae where descricao ilike concat('%', {token}, '%')"
                ),
            )
        ).all()

        # Map the results to the desired format
        cnae_dict = [
            {"code": cnae.codigo, "text": cnae.descricao} for cnae in cnae_result
        ]

        return cnae_dict

    def get_cnaes(
        self, limit: int = 10, offset: int = 0, enable_pagination: bool = True
    ):
        """
        Get all CNAEs from the database.

        Returns:
        DataFrame: The DataFrame with the CNAEs.
        """

        query = (
            text(
                f"""
                    select
                        codigo, descricao
                    from
                        cnae
                    limit
                        {limit}
                    offset
                        {offset}
                """
            )
            if enable_pagination
            else text(
                """
                    select
                        codigo, descricao
                    from
                        cnae
                """
            )
        )

        cnaes_result = self.session.execute(query)
        cnaes_result = cnaes_result.fetchall()

        columns = ["code", "text"]
        cnae_df = pd.DataFrame(cnaes_result, columns=columns)

        return cnae_df.to_dict(orient="records")

    def get_legal_nature(self, legal_nature_code: CodeType):
        """
        Get legal nature from the database.

        Returns:
        dict: The dictionary with the legal nature code and text.
        """
        is_valid_legal_nature_code = legal_nature_code or is_number(legal_nature_code)
        if not is_valid_legal_nature_code:
            return {}

        query = text(
            f"""
            select
                descricao
            from
                natju
            where
                codigo::text = '{legal_nature_code}'
            """
        )

        legal_natures_result = self.session.execute(query).fetchall()

        legal_nature_description = (
            "" if len(legal_natures_result) == 0 else legal_natures_result[0][0]
        )

        return (
            {}
            if len(legal_nature_description) == 0
            else {
                "code": legal_nature_code,
                "text": legal_nature_description,
            }
        )

    def get_legal_natures_list(self, legal_nature_list: CodeListType):
        """
        Get legal nature from the database.

        Returns:
        dict: The dictionary with the legal nature code and text.
        """
        legal_nature_str = ",".join(
            [f"'{str(legal_nature_code)}'" for legal_nature_code in legal_nature_list]
        )

        query = text(
            f"""
                select
                    distinct
                        codigo, descricao
                from
                    natju
                where
                    codigo::text in ({legal_nature_str})
            """
        )

        legal_natures_result = self.session.execute(query).fetchall()

        def wrap_values_map(code_text):
            return {"code": code_text[0], "text": code_text[1]}

        registration_status_dict = list(map(wrap_values_map, legal_natures_result))

        return registration_status_dict

    def get_legal_natures(
        self, limit: int = 10, offset: int = 0, enable_pagination: bool = True
    ):
        """
        Get all legal natures from the database.

        Returns:
        List: The List with the legal natures text and code.
        """

        query = (
            text(
                f"""
                    select
                        codigo, descricao
                    from
                        natju
                    limit
                        {limit}
                    offset
                        {offset}
                """
            )
            if enable_pagination
            else text(
                """
                    select
                        codigo, descricao
                    from
                        natju
                """
            )
        )

        legal_natures_result = self.session.execute(query).fetchall()

        columns = ["code", "text"]
        empty_df = pd.DataFrame(columns=columns)
        legal_natures_df = pd.DataFrame(legal_natures_result, columns=columns)
        legal_natures_df = empty_df if len(legal_natures_df) == 0 else legal_natures_df
        legal_natures_dict = legal_natures_df.to_dict(orient="records")

        return legal_natures_dict

    def get_registration_status_list(self, registration_status_codes: CodeListType):
        """
        Get the reason for the signup situation.

        Parameters:
        code (str): The code of the signup situation.

        Returns:
        str: The reason for the signup situation.
        """
        registration_status_str = ",".join(
            [
                f"'{str(registration_status_code)}'"
                for registration_status_code in registration_status_codes
            ]
        )

        query = text(
            f"""
                select
                    distinct
                        codigo,
                        descricao
                from
                    moti
                where
                    codigo::text in ({registration_status_str})
            """
        )

        registration_status_result = self.session.execute(query).fetchall()

        def wrap_values_map(code_text):
            return {"code": code_text[0], "text": code_text[1]}

        registration_status_dict = list(
            map(wrap_values_map, registration_status_result)
        )

        return registration_status_dict

    def get_registration_statuses(
        self, limit: int = 10, offset: int = 0, enable_pagination: bool = True
    ):
        """
        Get all registration statuses from the database.

        Returns:
        List: The List with the registration statuses.
        """
        query = (
            text(
                f"""
                    select
                        codigo, descricao
                    from
                        moti
                    limit {limit}
                    offset {offset}
                """
            )
            if enable_pagination
            else text(
                """
                    select
                        codigo, descricao
                    from
                        moti
                """
            )
        )

        reason_result = self.session.execute(query).fetchall()

        columns = ["code", "text"]
        empty_df = pd.DataFrame(columns=columns)
        reason_df = pd.DataFrame(reason_result, columns=columns)
        reason_df = empty_df if len(reason_df) == 0 else reason_df
        reason_dict = reason_df.to_dict(orient="records")

        return reason_dict

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
        if not city_code and not is_number(city_code):
            return {}

        query = text(
            f"""
                select
                    distinct codigo, descricao
                from
                    munic
                where
                    codigo = '{city_code}'
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

        return {} if len(city_df) == 0 else city_df.to_dict(orient="records")[0]

    def get_cities(self, limit: int = 10, offset: int = 0):
        """
        Get the city for the code.

        Parameters:
        code (str): The code of the city.

        Returns:
        str: The name of the city.
        """

        query = text(
            f"""
                select
                    codigo, descricao
                from
                    munic
                limit {limit}
                offset {offset}
            """
        )

        city_result = self.session.execute(query).fetchall()

        columns = ["code", "text"]
        empty_df = pd.DataFrame(columns=columns)
        city_df = (
            empty_df if not city_result else pd.DataFrame(city_result, columns=columns)
        )
        city_dict = city_df.to_dict(orient="records")

        return city_dict

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

        query = text(
            """
                select
                    descricao
                from
                    munic
            """
        )

        city_result = self.session.execute(query).fetchall()
        city_result = [city[0] for city in city_result]

        # NOTE: Hard coded limit_count = 3
        LIMIT_COUNT = 3

        return {
            city_candidate: find_most_possible_tokens(
                city_result, lower_city_candidate, LIMIT_COUNT
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
        cities_code_str = ",".join(
            [f"'{str(city_code)}'" for city_code in cities_code_list]
        )

        query = text(
            f"""
                select
                    codigo, descricao
                from
                    munic
                where
                    codigo::text in ({cities_code_str})
            """
        )

        city_result = self.session.execute(query).fetchall()

        def wrap_values_map(code_text):
            return {"code": code_text[0], "text": code_text[1]}

        cities_dict = list(map(wrap_values_map, city_result))

        return cities_dict

    def get_company_size_dict(self):
        """
        Get the company dictionary.

        Returns:
        - dict: The company dictionary.
        """
        return SIZE_DICT

    def get_establishment_type_dict(self):
        """
        Get the establishment type dictionary.

        Returns:
        - dict: The establishment type dictionary.
        """
        return EST_TYPE_DICT

    def get_company_situation_dict(self):
        """
        Get the company situation dictionary.

        Returns:
        - dict: The company situation dictionary.
        """
        return SITUATION_DICT

    def get_cnpjs_company(self, cnpj_list: CNPJList):
        """
        Get the company for the CNPJ.

        Parameters:
        cnpj (CNPJ): The CNPJ object.

        Returns:
        DataFrame: The DataFrame with the company.
        """
        cnpj_basicos = [cnpj_obj.basico_int for cnpj_obj in cnpj_list]
        cnpj_basicos_str = ",".join(
            [f"'{str(cnpj_basico)}'" for cnpj_basico in cnpj_basicos]
        )

        columns = [
            "cnpj_basico",
            "razao_social",
            "ente_federativo_responsavel",
            "porte_empresa",
            "capital_social",
            "natureza_juridica",
        ]
        columns_str = ", ".join(columns)

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

        company_result = self.session.execute(query)
        company_result = company_result.fetchall()

        company_result = replace_invalid_fields_on_list_tuple(company_result)
        company_result = replace_spaces_on_list_tuple(company_result)

        empty_df = pd.DataFrame(columns=columns)
        company_df = pd.DataFrame(company_result, columns=columns)
        company_df = empty_df if len(company_result) == 0 else company_df

        if len(company_df) == 0:
            return []

        company_df["efr"] = company_df["ente_federativo_responsavel"]
        company_df["nome"] = company_df["razao_social"]
        del company_df["razao_social"]
        del company_df["ente_federativo_responsavel"]

        capital_social = company_df["capital_social"]
        capital_social = capital_social.apply(format_decimal)

        company_df["capital_social"] = capital_social

        company_df["porte"] = (
            company_df["porte_empresa"]
            .apply(number_string_to_number)
            .apply(str)
            .map(SIZE_DICT)
        )
        del company_df["porte_empresa"]

        def zfill_8_map(value):
            return value.zfill(8)

        company_df["cnpj_basico"] = company_df["cnpj_basico"].apply(zfill_8_map)

        company_dict = dataframe_to_nested_dict(company_df, "cnpj_basico")

        cnpjs_base = [cnpj.to_tuple()[0] for cnpj in cnpj_list]

        companies_dict = {
            cnpj.to_raw(): company_dict[cnpj_base]
            for cnpj_base, cnpj in zip(cnpjs_base, cnpj_list)
        }

        return companies_dict

    def __format_establishment(self, establishment_dict: Dict):
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

        establishment_dict["situacao"] = SITUATION_DICT[situacao_cadastral]
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

        is_1_invalid = is_field_valid(ddd_1)
        is_2_invalid = is_field_valid(ddd_2)

        # Format the phone number
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
        establishment_dict["tipo"] = EST_TYPE_DICT[identificador]

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
        second_activities = establishment_dict["cnae_fiscal_secundaria"]
        if is_field_valid(second_activities):
            side_activities_str = establishment_dict["cnae_fiscal_secundaria"]

            side_activity_names = []
            for side_activity in side_activities_str.split(","):
                if len(side_activity) != 0:
                    side_activity_code = int(side_activity.strip())
                    side_activity_name = self.get_cnae(side_activity_code)
                    side_activity_names.append(side_activity_name)

            establishment_dict["atividades_secundarias"] = side_activity_names
        else:
            establishment_dict["atividades_secundarias"] = []

        del establishment_dict["cnae_fiscal_secundaria"]

        list_dict = [establishment_dict]
        list_dict = replace_invalid_fields_on_list_dict(list_dict)
        establishment_dict = list_dict[0]

        return establishment_dict

    def get_cnpjs_establishment(self, cnpj_list: CNPJList) -> Dict:
        cnpjs_basicos = [f"'{str(cnpj.basico_int)}'" for cnpj in cnpj_list]
        cnpjs_ordem = [f"'{str(cnpj.ordem_int)}'" for cnpj in cnpj_list]
        cnpjs_dv = [f"'{str(cnpj.digitos_verificadores_int)}'" for cnpj in cnpj_list]

        cnpjs_basicos_str = ",".join(cnpjs_basicos)
        cnpjs_ordem_str = ",".join(cnpjs_ordem)
        cnpjs_dv_str = ",".join(cnpjs_dv)

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
        columns_str = ",".join(columns)

        # Create the table if it does not exist
        query = text(
            f"""
                select
                    distinct on (cnpj_basico)
                    {columns_str}
                from
                    estabelecimento est
                where
                    est.cnpj_basico::text in ({cnpjs_basicos_str}) AND
                    est.cnpj_ordem::text in ({cnpjs_ordem_str}) AND
                    est.cnpj_dv::text in ({cnpjs_dv_str})
            """
        )

        establishment_result = self.session.execute(query)
        establishment_result = establishment_result.fetchall()

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

        registration_status = tuple(set(establishment_df["motivo_situacao_cadastral"]))
        registration_status = [f"'{status}'" for status in registration_status]
        registration_status_str = ",".join(registration_status)

        query = text(
            f"""
                select
                    codigo, descricao
                from
                    moti
                where
                    codigo::text in ({registration_status_str})
            """
        )

        registration_status_result = self.session.execute(query)
        registration_status_result = registration_status_result.fetchall()

        registration_status_dict = dict(registration_status_result)

        registration_status = establishment_df["motivo_situacao_cadastral"]
        registration_status = registration_status.map(registration_status_dict)
        establishment_df["motivo_situacao_cadastral"] = registration_status

        # Normalize data
        def zfill_map(value: str, num: int):
            return value.zfill(num)

        cnpj_base_series = establishment_df["cnpj_basico"]
        cnpj_ordem_series = establishment_df["cnpj_ordem"]
        cnpj_dv_series = establishment_df["cnpj_dv"]

        establishment_df["cnpj_"] = (
            cnpj_base_series.apply(lambda value: zfill_map(value, 8))
            + cnpj_ordem_series.apply(lambda value: zfill_map(value, 4))
            + cnpj_dv_series.apply(lambda value: zfill_map(value, 2))
        )
        establishment_dict = dataframe_to_nested_dict(establishment_df, "cnpj_")

        establishment_items = list(establishment_dict.items())

        def item_map(item):
            return item[0], self.__format_establishment(item[1])

        establishment_dict = dict(map(item_map, establishment_items))

        return establishment_dict

    def get_cnpj_establishments(self, cnpj: CNPJ) -> List:
        # Create the table if it does not exist
        query = text(
            f"""
                select
                    distinct cnpj_basico, cnpj_ordem, cnpj_dv, correio_eletronico,
                    data_inicio_atividade, data_situacao_cadastral, situacao_cadastral,
                    motivo_situacao_cadastral, nome_fantasia,
                    tipo_logradouro, logradouro, numero, complemento, bairro, municipio, cep, uf,
                    cnae_fiscal_principal, cnae_fiscal_secundaria, identificador_matriz_filial,
                    situacao_especial, data_situacao_especial,
                    ddd_1, telefone_1, ddd_2, telefone_2
                from
                    estabelecimento est
                where
                    est.cnpj_basico = '{cnpj.basico_int}'
                order by
                    1, 2
            """
        )

        establishment_result = self.session.execute(query)
        establishment_result = establishment_result.fetchall()

        establishment_result = replace_invalid_fields_on_list_tuple(
            establishment_result
        )
        establishment_result = replace_spaces_on_list_tuple(establishment_result)

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
        cnpj_basicos = [f"'{str(cnpj_obj.basico_int)}'" for cnpj_obj in cnpj_list]

        cnpj_basicos_str = ",".join(cnpj_basicos)

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

        partners_result = self.session.execute(query)
        partners_result = partners_result.fetchall()

        partners_result = replace_invalid_fields_on_list_tuple(partners_result)
        partners_result = replace_spaces_on_list_tuple(partners_result)

        columns = ["cnpj_basico", "qsa"]
        empty_df = pd.DataFrame(columns=columns)

        partners_df = pd.DataFrame(partners_result, columns=columns)
        partners_df = empty_df if len(partners_df) == 0 else partners_df

        def fill_8_map(cnpj):
            return cnpj.zfill(8)

        partners_df["qsa"] = partners_df["qsa"].apply(string_to_json)
        partners_df["cnpj_basico"] = partners_df["cnpj_basico"].apply(fill_8_map)
        partners_dict = dataframe_to_nested_dict(partners_df, index_col="cnpj_basico")

        cnpjs_raw_base = [(cnpj.to_raw(), cnpj.to_tuple()[0]) for cnpj in cnpj_list]

        empty_dict = {"qsa": []}

        def cnpj_map(cnpj_base_):
            return (
                partners_dict[cnpj_base_] if cnpj_base_ in partners_dict else empty_dict
            )

        partners_dict = {
            cnpj_raw: cnpj_map(cnpj_base) for cnpj_raw, cnpj_base in cnpjs_raw_base
        }

        return partners_dict

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

        activities_result = self.session.execute(query)
        activities_result = activities_result.fetchall()

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
            "ultima_atualizacao",
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
        ]

        # Get the establishment
        establishment_dict = self.get_cnpjs_establishment(cnpj_list)

        # Get company info
        company_dict = self.get_cnpjs_company(cnpj_list)

        # Get partners
        partners_dict = self.get_cnpjs_partners(cnpj_list)

        establ_list = list(establishment_dict)
        companies_list = list(company_dict)
        partners_list = list(partners_dict)

        common_keys = list(
            set(establ_list).intersection(companies_list).intersection(partners_list)
        )

        cnpj_info_dict = {
            common_key: {
                **establishment_dict[common_key],
                **company_dict[common_key],
                **partners_dict[common_key],
            }
            for common_key in common_keys
        }

        get_cnpj_scrap_service()

        # XXX: Fix scrap according to new route structure
        # update_at = cnpj_scrap_service.max_update_at()

        cnpj_infos = {
            cnpj_key: {
                "cnpj_raw": cnpj_key,
                # "ultima_atualizacao": update_at.strftime(date_format),
                **cnpj_info,
            }
            for cnpj_key, cnpj_info in cnpj_info_dict.items()
        }

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
        cnpj_base = cnpj.to_tuple()[0]

        columns = [
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
            "ultima_atualizacao",
        ]
        empty_df = pd.DataFrame(columns=columns)

        cnpj_list = [cnpj]

        # Get the establishment
        establishment_dict = self.get_cnpjs_establishment(cnpj_list)

        if not establishment_dict:
            return empty_df.to_dict(orient="records")

        establishment_dict = establishment_dict[cnpj_base]

        # Get company info
        company_dict = self.get_cnpjs_company(cnpj_list)
        company_dict = company_dict[cnpj_base]

        # Get partners
        partners_dict = self.get_cnpjs_partners(cnpj_list)
        partners_dict = partners_dict[cnpj_base]

        cnpj_info_dict = {**company_dict, **establishment_dict, **partners_dict}

        date_format = "%Y-%m-%d %H:%M:%S"
        cnpj_info_dict["ultima_atualizacao"] = datetime.now().strftime(date_format)

        return {key: cnpj_info_dict[key] for key in columns if key in cnpj_info_dict}

    def get_cnpjs_with_cnae(self, cnae_code: str, limit: int = 10, offset: int = 0):
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
        self, cnaes_list: CodeListType, limit: int = 10, offset: int = 0
    ):
        """
        Get the companies by the CNAEs.

        Parameters:
        cnaes_list (CodeListType): The list of CNAEs.

        Returns:
        Dict: The dictionary with the CNPJs info.
        """
        cnaes_str = ",".join([f"'{cnae}'" for cnae in cnaes_list])

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
        self, states_list: CodeListType, limit: int = 10, offset: int = 0
    ):
        """
        Get the companies by the states.

        Parameters:

        Returns:
        Dict: The dictionary with the CNPJs info.
        """

        states_str = ",".join([f"'{state}'" for state in states_list])

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
