from typing import Dict, Union
from sqlalchemy import text
import pandas as pd
from datetime import datetime

from backend.utils.misc import string_to_json
from backend.api.models.cnpj import CNPJ
from backend.database.base import Database
from backend.utils.misc import (
    replace_invalid_fields_on_list_tuple,
    replace_invalid_fields_on_list_dict,
    replace_spaces_on_list_tuple,
    format_decimal,
    replace_spaces,
    format_database_date,
    is_field_valid,
    format_cep,
    format_phone,
    is_number,
    number_string_to_number,
    humanize_string,
)

from backend.api.utils.cnpj import format_cnpj

# Constants
SIZE_DICT = {
    "0": "NÃO INFORMADO",
    "1": "MICRO EMPRESA",
    "3": "EMPRESA DE PEQUENO PORTE",
    "5": "DEMAIS",
}

SITUATION_DICT = {
    "1": "NULA",
    "2": "ATIVA",
    "3": "SUSPENSA",
    "4": "INAPTA",
    "8": "BAIXADA",
}

EST_TYPE_DICT = {
    "1": "MATRIZ", 
    "2": "FILIAL"
}

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

            return list(cnpjs_df.to_dict().values())[0]

    def get_cnae(self, cnae_code: str):
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
            query = text(f"select descricao from cnae where codigo = '{cnae_code}'")

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

    def get_cnaes(self, limit: int = 10, offset: int = 0, all: bool = False):
        """
        Get all CNAEs from the database.

        Returns:
        DataFrame: The DataFrame with the CNAEs.
        """

        with self.database.engine.begin() as connection:
            query = text(
                f"""
                    select
                        codigo, descricao
                    from cnae
                    limit {limit}
                    offset {offset}
                """
            )

            cnaes_result = connection.execute(query)
            cnaes_result = cnaes_result.fetchall()

            columns = ["code", "text"]
            cnae_df = pd.DataFrame(cnaes_result, columns=columns)

            return cnae_df.to_dict(orient="records")

    def get_legal_nature(self, legal_nature_code: str):
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
                f"select descricao from natju where codigo = '{legal_nature_code}'"
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

    def get_legal_natures(self, limit: int = 10, offset: int = 0, all: bool = False):
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
                    from natju
                    limit {limit}
                    offset {offset}
                """
                )
                if not all
                else text(
                    """
                    select
                        codigo, descricao
                    from natju
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

    def get_registration_status(self, registration_status_code: str):
        """
        Get the reason for the signup situation.

        Parameters:
        code (str): The code of the signup situation.

        Returns:
        str: The reason for the signup situation.
        """
        with self.database.engine.begin() as connection:
            query = text(
                f"select distinct descricao from moti where codigo = '{registration_status_code}'"
            )

            registration_status_result = connection.execute(query).fetchall()
            
            
            
            legal_nature_description = (
                ""
                if not registration_status_result
                else registration_status_result[0][0]
            )

            return (
                {}
                if len(legal_nature_description) == 0
                else {
                    "code": registration_status_code,
                    "text": legal_nature_description,
                }
            )

    def get_registration_statuses(
        self, limit: int = 10, offset: int = 0, all: bool = False
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
                    from moti
                    limit {limit}
                    offset {offset}
                """
                )
                if not all
                else text(
                    """
                    select
                        codigo, descricao
                    from moti
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
                f"select distinct codigo, descricao from munic where codigo = '{city_code}'"
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
                    from munic
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

    def get_company(self, cnpj: CNPJ):
        """
        Get the company for the CNPJ.

        Parameters:
        cnpj (CNPJ): The CNPJ object.

        Returns:
        DataFrame: The DataFrame with the company.
        """

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
                        where emp.cnpj_basico = '{cnpj.basico_int}'
                )
                select
                    distinct on (cnpj_basico)
                    cnpj_basico,
                    razao_social,
                    ente_federativo_responsavel,
                    porte_empresa,
                    capital_social,
                    concat(natju.codigo, '-', natju.descricao) as natureza_juridica
                from empresa_ emp
                left join natju
                    on natju.codigo = emp.natureza_juridica
                """
            )

            company_result = connection.execute(query)
            company_result = company_result.fetchall()

            company_result = replace_invalid_fields_on_list_tuple(company_result)
            company_result = replace_spaces_on_list_tuple(company_result)

            empty_df = pd.DataFrame(columns=columns)
            company_df = pd.DataFrame(company_result, columns=columns)
            company_df = empty_df if len(company_result) == 0 else company_df

            company_dict = company_df.to_dict(orient="records")[0]

            if len(company_df) == 0:
                return []

            del company_dict["cnpj_basico"]

            company_dict["efr"] = company_dict["ente_federativo_responsavel"]
            company_dict["nome"] = company_dict["razao_social"]
            del company_dict["razao_social"]
            del company_dict["ente_federativo_responsavel"]

            capital_social = company_dict["capital_social"]
            capital_social = format_decimal(capital_social)
            company_dict["capital_social"] = capital_social

            porte = str(number_string_to_number(company_dict["porte_empresa"]))
            company_dict["porte"] = SIZE_DICT[porte]

            del company_dict["porte_empresa"]

            return company_dict

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

        establishment_dict["email"]=establishment_dict["correio_eletronico"].lower()
        del establishment_dict["correio_eletronico"]
        
        basico = establishment_dict["cnpj_basico"].zfill(8)
        ordem = establishment_dict["cnpj_ordem"].zfill(4)
        dv = establishment_dict["cnpj_dv"].zfill(2)
        establishment_dict["cnpj"] = format_cnpj(f"{basico}{ordem}{dv}")

        del establishment_dict["cnpj_basico"]
        del establishment_dict["cnpj_ordem"]
        del establishment_dict["cnpj_dv"]

        # Get the registration status
        situacao_cadastral = str(
            number_string_to_number(
                establishment_dict["situacao_cadastral"]
            )
        )
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
        establishment_dict["motivo_situacao"] = establishment_dict["motivo_situacao_cadastral"]
        
        del establishment_dict["motivo_situacao_cadastral"]
        
        # Format the phone number
        # Check if the DDD columns are invalid
        ddd_1 = establishment_dict["ddd_1"]
        ddd_2 = establishment_dict["ddd_2"]
        telefone_1 = establishment_dict["telefone_1"]
        telefone_2 = establishment_dict["telefone_2"]

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
        address_type = replace_spaces(establishment_dict["tipo_logradouro"]).strip()
        address_name = replace_spaces(establishment_dict["logradouro"]).strip()
        address = humanize_string(address_type + " " + address_name)

        establishment_dict["logradouro"] = address
        del establishment_dict["tipo_logradouro"]

        # Format UF
        establishment_dict["complemento"] = humanize_string(establishment_dict["complemento"])
        establishment_dict["bairro"] = humanize_string(establishment_dict["bairro"])
        
        # Format CEP
        establishment_dict["cep"] = format_cep(establishment_dict["cep"])

        # Get the company type
        identificador = establishment_dict["identificador_matriz_filial"]
        establishment_dict["tipo"] = EST_TYPE_DICT[identificador]

        del establishment_dict["identificador_matriz_filial"]

        # Get city name
        city_code = establishment_dict["municipio"]
        city_dict = self.get_city(city_code)

        establishment_dict["municipio"] = humanize_string(city_dict["text"])

        # Get the main CNAE
        atividade_principal = establishment_dict["cnae_fiscal_principal"]

        establishment_dict["atividade_principal"] = (
            self.get_cnae(atividade_principal) if atividade_principal else {}
        )

        del establishment_dict["cnae_fiscal_principal"]

        # Get the secondary CNAEs
        second_activities = establishment_dict["cnae_fiscal_secundaria"]
        if is_field_valid(second_activities):
            atividade_principal_str = establishment_dict["cnae_fiscal_secundaria"]

            second_activities = []
            for atividade in atividade_principal_str.split(","):
                second_activities.append(self.get_cnae(atividade))

            establishment_dict["atividades_secundarias"] = second_activities
        else:
            establishment_dict["atividades_secundarias"] = []

        del establishment_dict["cnae_fiscal_secundaria"]

        return establishment_dict

    def get_establishment(self, cnpj: CNPJ) -> Union[Dict[str, str], None]:
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
            columns_str=", ".join(columns)
            
            # Create the table if it does not exist
            query = text(
                f"""
                    select
                        distinct on (cnpj_basico) 
                        {columns_str}
                    from estabelecimento est
                    where
                        est.cnpj_basico = '{cnpj.basico_int}' AND
                        est.cnpj_ordem = '{cnpj.ordem_int}' AND
                        est.cnpj_dv = '{cnpj.digitos_verificadores_int}'
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
                    from moti
                    where
                        codigo = '{registration_status}'
                """
            )

            registration_status_result = connection.execute(query)
            registration_status_result = registration_status_result.fetchall()

            registration_status_descrip = registration_status_result[0][0]

        establishment_df = pd.DataFrame(establishment_result, columns=columns)
        establishment_df = (
            empty_df 
            if len(establishment_result) == 0 else establishment_df
        )
        establishment_dict = establishment_df.to_dict(orient="records")[0]
        establishment_dict["motivo_situacao_cadastral"] = registration_status_descrip

        # Normalize data
        
        return self.__format_establishment(establishment_dict)

    def get_establishments(self, cnpj: CNPJ):
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
                        est.cnpj_basico = '{cnpj.basico_int}'
                """
            )

            establishment_result = connection.execute(query)
            establishment_result = establishment_result.fetchall()

            establishment_result = replace_invalid_fields_on_list_tuple(
                establishment_result
            )
            establishment_result = replace_spaces_on_list_tuple(establishment_result)

        columns = [
            "cnpj_basico",
            "cnpj_ordem",
            "cnpj_dv",
            "email",
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
        establishment_list = establishment_df.to_dict(orient="records")

        est_is_empty = len(establishment_df) == 0
        return (
            []
            if est_is_empty
            else list(map(self.__format_establishment, establishment_list))
        )

    def get_partners(self, cnpj: CNPJ):
        """
        Get the partners for the CNPJ.

        Parameters:
        cnpj (CNPJ): The CNPJ object.

        Returns:
        DataFrame: The DataFrame with the partners.
        """

        with self.database.engine.begin() as connection:
            query = text(
                f"""
                    with socios_ as (
                        select
                            cnpj_basico,
                            qualificacao_socio,
                            nome_socio_razao_social
                        from socios
                        where cnpj_basico = '{cnpj.basico_int}'
                        group by 1, 2, 3
                    )
                    SELECT 
                        cnpj_basico,
                        json_agg(
                            json_build_object(
                                'nome', nome_socio_razao_social,
                                'qual', concat(qualificacao_socio,'-', qual_socio.descricao)
                            )
                        ) AS qsa
                    FROM socios_ soc
                    left join quals qual_socio
                        on qual_socio.codigo = soc.qualificacao_socio
                    GROUP BY cnpj_basico
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

            partners_dict = partners_df.to_dict(orient="records")[0]
            partners_list = string_to_json(partners_dict["qsa"])

            partners_list = replace_invalid_fields_on_list_dict(partners_list)

            return {"qsa": partners_list}

    def get_activities(self, cnpj: CNPJ):
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
                            ) AS codigo_cnae
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
                    from atividades_secundarias a_s
                    inner join atividade_principal a_p
                    on a_s.cnpj_basico::text = a_p.cnpj_basico::text
                """
            )
            
            activities_result = connection.execute(query)
            activities_result = activities_result.fetchall()
            
            activities_result = replace_invalid_fields_on_list_tuple(activities_result)
            activities_result = replace_spaces_on_list_tuple(activities_result)
            print(activities_result)
            columns = ["cnpj_basico", "atividade_principal", "atividades_secundarias"]
            partners_df = pd.DataFrame(activities_result, columns=columns)
            empty_df = pd.DataFrame(columns=columns)

            partners_df = empty_df if len(partners_df) == 0 else partners_df

            partners_dict = partners_df.to_dict(orient="records")[0]

            main_activities = string_to_json(partners_dict["atividade_principal"])
            secondary_activities = string_to_json(
                partners_dict["atividades_secundarias"]
            )

            is_empty = len(secondary_activities) == 1 and secondary_activities[0] == {}
            atividades_secundarias = [] if is_empty else secondary_activities

            return {
                "atividade_principal": main_activities,
                "atividades_secundarias": atividades_secundarias,
            }

    def get_cnpj_info(self, cnpj: CNPJ) -> Dict[str, str]:
        """
        Get the information for the CNPJ.

        Parameters:
        cnpj (CNPJ): The CNPJ object.

        Returns:
        dict: The dictionary with the CNPJ information.
        """
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

        # Get the establishment
        establishment_dict = self.get_establishment(cnpj)

        if not establishment_dict:
            return empty_df.to_dict(orient="records")

        # Get company info
        company_dict = self.get_company(cnpj)
        
        # Get partners
        partners_dict = self.get_partners(cnpj)

        cnpj_info_dict = {**establishment_dict, **company_dict, **partners_dict}

        cnpj_info_dict["ultima_atualizacao"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        return {key: cnpj_info_dict[key] for key in columns if key in cnpj_info_dict}

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
            "uf",
            "cep",
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
                            cnae_fiscal_principal = '{cnae_code}' or
                            cnae_fiscal_secundaria like '%{cnae_code}%'
                        ) and 
                        situacao_cadastral = '2' -- ATIVA
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
            this_registration_status=tuple({comp[7] for comp in est_result})
            this_registration_status_str=", ".join(this_registration_status)

            query = text(
                f"""
                    select
                        codigo, descricao
                    from 
                        moti
                    where 
                        codigo in ({this_registration_status_str})
                """
            )

            registration_status_result = connection.execute(query)
            registration_status_result = registration_status_result.fetchall()
            
            registration_status_dict=dict(registration_status_result)
            registration_status_dict={str(k):v for k,v in registration_status_dict.items()}

            registration_map=lambda x: f"{x}-{registration_status_dict[x]}"
            df_est['motivo_situacao'] = df_est['motivo_situacao_cadastral'].map(registration_status_dict)
            
            # Get companies information 
            this_estab_cnpj = tuple({estab[0] for estab in est_result})

            columns = [
                "cnpj_basico",
                "razao_social",
                "ente_federativo_responsavel",
                "porte_empresa",
                "capital_social",
                "natureza_juridica",
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
                        cnpj_basico in {this_estab_cnpj}
                """
            )

            comp_result = connection.execute(query)
            comp_result = comp_result.fetchall()
            
            # Get the nature of the legal entity
            this_natjus=tuple({comp[5] for comp in comp_result})
            this_natjus_str=", ".join(map(str, this_natjus))
            
            query = text(
                f"""
                    select
                        codigo, descricao
                    from 
                        natju
                    where 
                        codigo in ({this_natjus_str})
                """
            )
            
            natju_result = connection.execute(query)
            natju_result = natju_result.fetchall()
            
            natju_dict=dict(natju_result)    
            natju_dict={str(k):v for k,v in natju_dict.items()}        
            
            comp_result = replace_invalid_fields_on_list_tuple(comp_result)
            comp_result = replace_spaces_on_list_tuple(comp_result)

            comp_df = pd.DataFrame(comp_result, columns=columns)
            
            df_comp = empty_df if len(comp_result) == 0 else comp_df
            legal_nature_map=lambda x: f"{x}-{natju_dict[x]}"
            df_comp['natureza_juridica'] = df_comp['natureza_juridica'].apply(legal_nature_map)
            
            df_comp['porte_empresa']=df_comp['porte_empresa'].apply(number_string_to_number)
            df_comp['porte_empresa']=df_comp['porte_empresa'].apply(str)
            df_comp['porte'] = df_comp['porte_empresa'].map(SIZE_DICT)
            df_comp['porte'] = df_comp['porte'].apply(humanize_string)
            df_comp['razao_social'] = df_comp['razao_social'].apply(humanize_string)            
            df_comp['capital_social'] = df_comp['capital_social'].apply(format_decimal)
            
            remaining_columns=[
                column
                for column in df_comp.columns
                if column not in ['porte_empresa']
            ]
            df_comp=df_comp[remaining_columns]
            
            df = pd.merge(df_est, df_comp, on="cnpj_basico", how="left")
            records_dict = df.to_dict(orient="records")
            
            records_dicts = replace_invalid_fields_on_list_dict(records_dict)            
            records_dicts = list(map(self.__format_establishment, records_dicts))
            
            return records_dicts
