from typing import Dict, Union, List, Any
from sqlalchemy import text
import pandas as pd
from datetime import datetime

from backend.app.utils.misc import string_to_json
from backend.app.api.models.cnpj import CNPJ
from backend.app.database.base import Database
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
from backend.app.utils.repositories import (
    format_database_date,
    format_phone,
    format_cep,
)
from backend.app.utils.dataframe import dataframe_to_nested_dict
from backend.app.api.utils.cnpj import format_cnpj
from backend.app.repositories.constants import (
    SIZE_DICT, SITUATION_DICT, EST_TYPE_DICT,
)

# Types
CNPJList = List[CNPJ]
JSON = Dict[str, Any]
CodeType = Union[str, int]
CodeListType = List[CodeType]


class CNPJRepository:
    def __init__(self, uri: str):
        self.uri = uri
        self.database = Database(uri)

    def get_cnpjs(self, limit: int = 10, offset: int = 0):
        """
        Get all CNPJs from the database.

        Returns:
        DataFrame: The DataFrame with the CNPJs.
        """

        with self.database.engine.begin() as connection:
            query = text(
                f"""
                    select
                        concat(
                            lpad(cnpj_basico::text, 8, '0'),
                            lpad(cnpj_ordem::text, 4, '0'),
                            lpad(cnpj_dv::text, 2, '0')
                        ) as cnpj
                    from estabelecimento
                    limit {limit}
                    offset {offset}
                """
            )

            cnpjs_result = connection.execute(query)
            cnpjs_result = cnpjs_result.fetchall()

            cnpjs_result = replace_invalid_fields_on_list_tuple(cnpjs_result)

            columns = ["cnpj"]
            cnpjs_df = pd.DataFrame(cnpjs_result, columns=columns)
            
            cnpjs_list=list(cnpjs_df['cnpj'])

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

        with self.database.engine.begin() as connection:
            query = text(f"""
                select 
                    descricao 
                from 
                    cnae 
                where 
                    codigo::text = '{cnae_code}'             
            """)

            cnae_result = connection.execute(query).fetchall()

            cnae_description = "" if len(cnae_result) == 0 else cnae_result[0][0]

            return (
                {}
                if len(cnae_description) == 0
                else {
                    "code": cnae_code,
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
        cnae_code_str = ",".join([
            f"\'{str(cnae_code)}\'" 
            for cnae_code in cnae_code_list
        ])

        with self.database.engine.begin() as connection:
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

            cnae_result = connection.execute(query).fetchall()

        def wrap_values_map(code_text):
            return {"code": code_text[0], "text": code_text[1]}

        cnae_dict = list(map(wrap_values_map, cnae_result))

        return cnae_dict

    def get_cnaes(self, limit: int = 10, offset: int = 0, enable_pagination: bool = True):
        """
        Get all CNAEs from the database.

        Returns:
        DataFrame: The DataFrame with the CNAEs.
        """

        with self.database.engine.begin() as connection:
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

            cnaes_result = connection.execute(query)
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

        with self.database.engine.begin() as connection:
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
            

            legal_natures_result = connection.execute(query).fetchall()

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
            [
                f"\'{str(legal_nature_code)}\'" 
                for legal_nature_code in legal_nature_list
            ]
        )

        with self.database.engine.begin() as connection:
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

            legal_natures_result = connection.execute(query).fetchall()

        def wrap_values_map(code_text):
            return {
                "code": code_text[0], 
                "text": code_text[1]
            }

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

        with self.database.engine.begin() as connection:
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

            legal_natures_result = connection.execute(query).fetchall()

            columns = ["code", "text"]
            empty_df = pd.DataFrame(columns=columns)
            legal_natures_df = pd.DataFrame(legal_natures_result, columns=columns)
            legal_natures_df = (
                empty_df if len(legal_natures_df) == 0 else legal_natures_df
            )
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
                f"\'{str(registration_status_code)}\'"
                for registration_status_code in registration_status_codes
            ]
        )

        with self.database.engine.begin() as connection:
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

            registration_status_result = connection.execute(query).fetchall()

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

        with self.database.engine.begin() as connection:
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

            reason_result = connection.execute(query).fetchall()

            columns = ["code", "text"]
            empty_df = pd.DataFrame(columns=columns)
            reason_df = pd.DataFrame(reason_result, columns=columns)
            reason_df = empty_df if len(reason_df) == 0 else reason_df
            reason_dict = reason_df.to_dict(orient="records")

            return reason_dict

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

        with self.database.engine.begin() as connection:
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

            city_result = connection.execute(query).fetchall()

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

        with self.database.engine.begin() as connection:
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

            city_result = connection.execute(query).fetchall()

            columns = ["code", "text"]
            empty_df = pd.DataFrame(columns=columns)
            city_df = (
                empty_df
                if not city_result
                else pd.DataFrame(city_result, columns=columns)
            )
            city_dict = city_df.to_dict(orient="records")

            return city_dict

    def get_cities_list(self, cities_code_list: CodeListType):
        """
        Get the list of city object by the code.

        Parameters:
        code (CodeListType): The code of the city.

        Returns:
        List[dict]: The name of the city.
        """
        cities_code_str = ",".join([
            f"\'{str(city_code)}\'" 
            for city_code in cities_code_list
        ])

        with self.database.engine.begin() as connection:
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

            city_result = connection.execute(query).fetchall()

        def wrap_values_map(code_text):
            return {"code": code_text[0], "text": code_text[1]}

        cities_dict = list(map(wrap_values_map, city_result))

        return cities_dict

    def get_cnpjs_company(self, cnpj_list: CNPJList):
        """
        Get the company for the CNPJ.

        Parameters:
        cnpj (CNPJ): The CNPJ object.

        Returns:
        DataFrame: The DataFrame with the company.
        """
        cnpj_basicos = [f"\'{str(cnpj_obj.basico_int)}\'" for cnpj_obj in cnpj_list]
        cnpj_basicos_str = ",".join(cnpj_basicos)

        with self.database.engine.begin() as connection:
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
                        where emp.cnpj_basico::text in ({cnpj_basicos_str})
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

            company_result = connection.execute(query)
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

            cnpjs_base = [
                cnpj.to_tuple()[0] for cnpj in cnpj_list
            ]
            
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
                side_activity_code = side_activity.strip()

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

    def get_cnpj_establishment(self, cnpj: CNPJ) -> JSON:
        """
        Get the establishment for the CNPJ.

        Parameters:
            cnpj (CNPJ): The CNPJ object.

        Returns:
            DataFrame: The DataFrame with the establishment.
        """

        with self.database.engine.begin() as connection:
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
                        est.cnpj_basico::text = '{cnpj.basico_int}' AND
                        est.cnpj_ordem::text = '{cnpj.ordem_int}' AND
                        est.cnpj_dv::text = '{cnpj.digitos_verificadores_int}'
                """
            )

            establishment_result = connection.execute(query)
            establishment_result = establishment_result.fetchall()

            empty_df = pd.DataFrame(columns=columns)
            df_is_empty = len(establishment_result) == 0
            if df_is_empty:
                return None

            establishment_result = replace_invalid_fields_on_list_tuple(
                establishment_result
            )
            establishment_result = replace_spaces_on_list_tuple(establishment_result)

            registration_status = establishment_result[0][7]

            query = text(
                f"""
                    select
                        descricao
                    from 
                        moti
                    where
                        codigo::text = '{registration_status}'
                """
            )

            registration_status_result = connection.execute(query)
            registration_status_result = registration_status_result.fetchall()

            registration_status_descrip = registration_status_result[0][0]

        establishment_df = pd.DataFrame(establishment_result, columns=columns)
        establishment_df = (
            empty_df if len(establishment_result) == 0 else establishment_df
        )
        establishment_dict = establishment_df.to_dict(orient="records")[0]
        establishment_dict["motivo_situacao_cadastral"] = registration_status_descrip

        # Normalize data
        return self.__format_establishment(establishment_dict)

    def get_cnpjs_establishment(self, cnpj_list: CNPJList) -> Dict:
        cnpjs_basicos = [f"\'{str(cnpj.basico_int)}\'" for cnpj in cnpj_list]
        cnpjs_ordem = [f"\'{str(cnpj.ordem_int)}\'" for cnpj in cnpj_list]
        cnpjs_dv = [f"\'{str(cnpj.digitos_verificadores_int)}\'" for cnpj in cnpj_list]

        cnpjs_basicos_str = ",".join(cnpjs_basicos)
        cnpjs_ordem_str = ",".join(cnpjs_ordem)
        cnpjs_dv_str = ",".join(cnpjs_dv)

        with self.database.engine.begin() as connection:
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

            establishment_result = connection.execute(query)
            establishment_result = establishment_result.fetchall()

            empty_df = pd.DataFrame(columns=columns)
            df_is_empty = len(establishment_result) == 0
            if df_is_empty:
                return {}

            establishment_result = replace_invalid_fields_on_list_tuple(establishment_result)
            establishment_result = replace_spaces_on_list_tuple(establishment_result)

            establishment_df = pd.DataFrame(establishment_result, columns=columns)
            establishment_df = (empty_df if len(establishment_result) == 0 else establishment_df)

            registration_status = tuple(set(establishment_df["motivo_situacao_cadastral"]))
            registration_status=[ f"\'{status}\'" for status in registration_status ]
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

            registration_status_result = connection.execute(query)
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
            cnpj_base_series.apply(lambda value: zfill_map(value, 8)) + \
            cnpj_ordem_series.apply(lambda value: zfill_map(value, 4)) + \
            cnpj_dv_series.apply(lambda value: zfill_map(value, 2))
        )
        establishment_dict = dataframe_to_nested_dict(establishment_df, "cnpj_")

        establishment_items = list(establishment_dict.items())

        def item_map(item):
            return item[0], self.__format_establishment(item[1])

        establishment_dict = dict(map(item_map, establishment_items))
        
        return establishment_dict

    def get_cnpj_establishments(self, cnpj: CNPJ) -> List:
        with self.database.engine.begin() as connection:
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
                        est.cnpj_basico::text = '{cnpj.basico_int}'
                """
            )

            establishment_result = connection.execute(query)
            establishment_result = establishment_result.fetchall()

            establishment_result = replace_invalid_fields_on_list_tuple(
                establishment_result
            )
            establishment_result = replace_spaces_on_list_tuple(establishment_result)

        columns = [
            "cnpj_basico", "cnpj_ordem", "cnpj_dv", "correio_eletronico",
            "data_inicio_atividade","data_situacao_cadastral",
            "situacao_cadastral","motivo_situacao_cadastral", "nome_fantasia",
            "tipo_logradouro","logradouro","numero","complemento","bairro","municipio","cep","uf",
            "cnae_fiscal_principal", "cnae_fiscal_secundaria", "identificador_matriz_filial",
            "situacao_especial", "data_situacao_especial",
            "ddd_1", "telefone_1", "ddd_2", "telefone_2",
        ]
        empty_df = pd.DataFrame(columns=columns)
        establishment_df = pd.DataFrame(establishment_result, columns=columns)
        establishment_df = (
            empty_df if len(establishment_result) == 0 else establishment_df
        )

        establishment_df = establishment_df.sort_values(by=["cnpj_ordem"])
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
        cnpj_basicos = [
            f"\'{str(cnpj_obj.basico_int)}\'" 
            for cnpj_obj in cnpj_list
        ]

        cnpj_basicos_str = ",".join(cnpj_basicos)

        with self.database.engine.begin() as connection:
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
                            cnpj_basico::text IN ({cnpj_basicos_str})
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

            partners_result = connection.execute(query)
            partners_result = partners_result.fetchall()

            partners_result = replace_invalid_fields_on_list_tuple(partners_result)
            partners_result = replace_spaces_on_list_tuple(partners_result)

            columns = ["cnpj_basico", "qsa"]
            empty_df = pd.DataFrame(columns=columns)
            partners_df = pd.DataFrame(partners_result, columns=columns)
            partners_df = empty_df if len(partners_df) == 0 else partners_df

            if len(partners_df) == 0:
                return []

            def fill_8_map(cnpj):
                return cnpj.zfill(8)

            partners_df["qsa"] = partners_df["qsa"].apply(string_to_json)
            partners_df["cnpj_basico"] = partners_df["cnpj_basico"].apply(fill_8_map)
            partners_dict = dataframe_to_nested_dict(partners_df, index_col="cnpj_basico")

            cnpjs_raw_base = [
                (cnpj.to_raw(), cnpj.to_tuple()[0]) for cnpj in cnpj_list
            ]
            
            partners_dict = {
                cnpj_raw: partners_dict[cnpj_base]
                for cnpj_raw, cnpj_base in cnpjs_raw_base
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
        with self.database.engine.begin() as connection:
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
                                'code', cnae.codigo,
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

            activities_result = connection.execute(query)
            activities_result = activities_result.fetchall()

            activities_result = replace_invalid_fields_on_list_tuple(activities_result)
            activities_result = replace_spaces_on_list_tuple(activities_result)

            columns = ["cnpj_basico", "atividade_principal", "atividades_secundarias"]
            partners_df = pd.DataFrame(activities_result, columns=columns)
            empty_df = pd.DataFrame(columns=columns)

            partners_df = empty_df if len(partners_df) == 0 else partners_df

            partners_dict = partners_df.to_dict(orient="records")[0]


            main_activities_str=partners_dict["atividade_principal"]
            side_activities_str=partners_dict["atividades_secundarias"]
            main_activities = string_to_json(main_activities_str)
            side_activities = string_to_json(side_activities_str)

            is_empty = len(side_activities) == 1 and side_activities[0] == {}
            side_activities = [] if is_empty else side_activities

            return {
                "atividade_principal": main_activities,
                "atividades_secundarias": side_activities,
            }

    def get_cnpj_info(self, cnpj: CNPJ) -> JSON:
        """
        Get the information for the CNPJ.

        Parameters:
        cnpj (CNPJ): The CNPJ object.

        Returns:
        dict: The dictionary with the CNPJ information.
        """
        cnpj_base, cnpj_order, cnpj_digits = cnpj.to_tuple()

        columns = [
            "cnpj", "abertura", 
            "situacao", "data_situacao", "motivo_situacao", "situacao_especial", "data_situacao_especial",
            "tipo", "nome", "fantasia", "porte", "natureza_juridica", "capital_social",
            "atividade_principal", "atividades_secundarias",
            "logradouro", "numero","complemento","municipio","bairro","uf","cep",
            "email", "telefone", "efr", "qsa", "ultima_atualizacao",
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

        cnpj_info_dict = {**establishment_dict, **company_dict, **partners_dict}

        date_format = "%Y-%m-%d %H:%M:%S"
        cnpj_info_dict["ultima_atualizacao"] = datetime.now().strftime(date_format)

        return {
            key: cnpj_info_dict[key] 
            for key in columns if key in cnpj_info_dict
        }

    def get_cnpjs_info(self, cnpjs: CNPJList) -> JSON:
        """
        Get the information for the CNPJ.

        Parameters:
        cnpj (CNPJ): The CNPJ object.

        Returns:
        dict: The dictionary with the CNPJ information.
        """
        [
            cnpj.to_tuple() for cnpj in cnpjs
        ]
        cnpj_base, cnpj_order, cnpj_digits = cnpj.to_tuple()

        columns = [
            "cnpj", "abertura", 
            "situacao", "data_situacao", "motivo_situacao", "situacao_especial", "data_situacao_especial",
            "tipo", "nome", "fantasia", "porte", "natureza_juridica", "capital_social",
            "atividade_principal", "atividades_secundarias",
            "logradouro", "numero","complemento","municipio","bairro","uf","cep",
            "email", "telefone", "efr", "qsa", "ultima_atualizacao",
        ]
        empty_df = pd.DataFrame(columns=columns)

        cnpj_list = cnpjs

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

        cnpj_info_dict = {**establishment_dict, **company_dict, **partners_dict}

        date_format = "%Y-%m-%d %H:%M:%S"
        cnpj_info_dict["ultima_atualizacao"] = datetime.now().strftime(date_format)

        return {
            key: cnpj_info_dict[key] 
            for key in columns if key in cnpj_info_dict
        }

    def get_establishments_by_cnae(
        self, cnae_code: str, limit: int = 10, offset: int = 0
    ):
        """
        Get the companies with the CNAE.

        Parameters:
        cnae_code (str): The code of the CNAE.

        Returns:
        DataFrame: The DataFrame with the companies.
        """
        columns = [
            "cnpj_basico", "cnpj_ordem", "cnpj_dv", "correio_eletronico", "data_inicio_atividade",
            "data_situacao_cadastral","situacao_cadastral","motivo_situacao_cadastral","nome_fantasia",
            "tipo_logradouro", "logradouro", "numero", "complemento", "bairro", "municipio", "uf", "cep",
            "cnae_fiscal_principal", "cnae_fiscal_secundaria", "identificador_matriz_filial",
            "situacao_especial", "data_situacao_especial",
            "ddd_1", "telefone_1", "ddd_2", "telefone_2",
        ]
        columns_str = ", ".join(columns)

        with self.database.engine.begin() as connection:
            query = text(
                f"""
                    select 
                        distinct on (cnpj_basico)
                        {columns_str}
                    from 
                        estabelecimento
                    where 
                        (
                            cnae_fiscal_principal::text = '{cnae_code}' or
                            cnae_fiscal_secundaria like '%{cnae_code}%'
                        ) and 
                        situacao_cadastral::text = '2' -- ATIVA
                    order by
                        1
                    limit 
                        {limit} 
                    offset 
                        {offset}
                """
            )

            est_result = connection.execute(query)
            est_result = est_result.fetchall()

            est_result = replace_invalid_fields_on_list_tuple(est_result)
            est_result = replace_spaces_on_list_tuple(est_result)

            empty_df = pd.DataFrame(columns=columns)
            df_est = (
                empty_df
                if len(est_result) == 0
                else pd.DataFrame(est_result, columns=columns)
            )

            # Get the registration status
            this_registration_status = tuple({comp[7] for comp in est_result})
            this_registration_status = [
                f"\'{status}\'" for status in this_registration_status
            ]
            this_registration_status_str = ", ".join(this_registration_status)

            query = text(
                f"""
                    select
                        codigo, descricao
                    from 
                        moti
                    where 
                        codigo::text in ({this_registration_status_str})
                """
            )

            registration_status_result = connection.execute(query)
            registration_status_result = registration_status_result.fetchall()

            registration_status_dict = dict(registration_status_result)
            registration_status_dict = {
                str(k): v for k, v in registration_status_dict.items()
            }

            def registration_map(x):
                return f"{x}-{registration_status_dict[x]}"

            df_est["motivo_situacao"] = df_est["motivo_situacao_cadastral"].map(
                registration_status_dict
            )

            # Get companies information
            this_estab_cnpj = tuple({estab[0] for estab in est_result})

            columns = [
                "cnpj_basico", "razao_social", "ente_federativo_responsavel",
                "porte_empresa", "capital_social", "natureza_juridica",
            ]
            columns_str = ",".join(columns)

            query = text(
                f"""
                    select
                        distinct on (cnpj_basico)
                        {columns_str}
                    from 
                        empresa
                    where 
                        cnpj_basico::text in {this_estab_cnpj}
                """
            )

            comp_result = connection.execute(query)
            comp_result = comp_result.fetchall()

            # Get the nature of the legal entity
            this_natjus = tuple({comp[5] for comp in comp_result})
            this_natjus = [
                f"\'{str(natju)}\'" 
                for natju in this_natjus
            ]
            this_natjus_str = ", ".join(map(str, this_natjus))

            query = text(
                f"""
                    select
                        codigo, descricao
                    from 
                        natju
                    where 
                        codigo::text in ({this_natjus_str})
                """
            )

            natju_result = connection.execute(query)
            natju_result = natju_result.fetchall()

            natju_dict = dict(natju_result)
            natju_dict = {
                str(k): v 
                for k, v in natju_dict.items()
            }

            comp_result = replace_invalid_fields_on_list_tuple(comp_result)
            comp_result = replace_spaces_on_list_tuple(comp_result)

            comp_df = pd.DataFrame(comp_result, columns=columns)

            df_comp = empty_df if len(comp_result) == 0 else comp_df

            def legal_nature_map(x):
                return f"{x}-{natju_dict[x]}"

            df_comp["natureza_juridica"] = df_comp["natureza_juridica"].apply(
                legal_nature_map
            )

            df_comp["porte_empresa"] = df_comp["porte_empresa"].apply(
                number_string_to_number
            )
            df_comp["porte_empresa"] = df_comp["porte_empresa"].apply(str)
            df_comp["porte"] = df_comp["porte_empresa"].map(SIZE_DICT)
            df_comp["porte"] = df_comp["porte"].apply(humanize_string)
            df_comp["razao_social"] = df_comp["razao_social"].apply(humanize_string)
            df_comp["capital_social"] = df_comp["capital_social"].apply(format_decimal)

            remaining_columns = [
                column for column in df_comp.columns if column not in ["porte_empresa"]
            ]
            df_comp = df_comp[remaining_columns]

            df = pd.merge(df_est, df_comp, on="cnpj_basico", how="left")
            records_dict = df.to_dict(orient="records")

            records_dicts = replace_invalid_fields_on_list_dict(records_dict)
            records_dicts = list(map(self.__format_establishment, records_dicts))

            return records_dicts
