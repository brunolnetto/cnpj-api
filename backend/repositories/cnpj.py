from typing import Dict
from sqlalchemy import text
import pandas as pd

from backend.api.models.cnpj import CNPJ
from backend.database.base import Database
from backend.utils.misc import (
    replace_spaces, 
    replace_nan_on_list_tuple,
    replace_spaces_on_list_tuple,
    is_database_field_valid,
    format_database_date,
    format_cep,
    format_phone
)

class CNPJRepository:
    def __init__(self, uri: str):
        self.uri = uri
        self.database = Database(uri)

    def test_connection(self):
        """
        Test the database connection.
        
        Returns:
        str: A message indicating the connection status.
        """
        with self.database.engine.begin() as connection:
            return "Conexão com o banco de dados estabelecida."

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
                        lpad(cnpj_basico::text, 8, '0') as cnpj_basico,
                        lpad(cnpj_ordem::text, 4, '0') as cnpj_ordem,
                        lpad(cnpj_dv::text, 2, '0') as cnpj_dv
                    from estabelecimento
                    limit {limit}
                    offset {offset}
                """
            )
            
            cnpjs_result = connection.execute(query)
            cnpjs_result = cnpjs_result.fetchall()
            cnpjs_result=replace_nan_on_list_tuple(cnpjs_result)
            
            columns = ["cnpj_basico", "cnpj_ordem", "cnpj_dv"]
            
            return pd.DataFrame(cnpjs_result, columns=columns)
    
    def get_cnae_description(self, cnae_code: str):
        """
        Get the CNAE for the code.
        
        Parameters:
        cnae_code (str): The code of the CNAE.
        
        Returns:
        str: The description of the CNAE.
        """
        
        with self.database.engine.begin() as connection:
            query = text(
                f"""
                    select descricao
                    from cnae
                    where codigo = '{cnae_code}'
                """
            )
            
            cnae_result = connection.execute(query)
            cnae_result = cnae_result.fetchall()[0][0]
            
            return cnae_result if len(cnae_result)!=0 else None
    
    def get_establishments_with_cnae(self, cnae_code: str, limit: int = 10, offset: int = 0):
        """
        Get the companies with the CNAE.
        
        Parameters:
        cnae_code (str): The code of the CNAE.
        
        Returns:
        DataFrame: The DataFrame with the companies.
        """
        
        columns=[
            "cnpj_basico", "cnpj_ordem", "cnpj_dv", "correio_eletronico",
            "data_inicio_atividade",  "data_situacao_cadastral", "situacao_cadastral", "motivo_situacao_cadastral", 
            "nome_fantasia", "tipo_logradouro", "logradouro", "numero", "complemento", "bairro", "municipio", "cep", "uf",
            "cnae_fiscal_principal", "cnae_fiscal_secundaria", "identificador_matriz_filial", 
            "situacao_especial", "data_situacao_especial",
            "ddd_1", "telefone_1", "ddd_2", "telefone_2"
        ]
        columns_str = ", ".join(columns)
        
        with self.database.engine.begin() as connection:
            query = text(
                f"""
                    select
                        {columns_str}
                    from estabelecimento
                    where cnae_fiscal_principal = '{cnae_code}' and 
                        situacao_cadastral = '2' 
                    order by 1
                    limit {limit} 
                    offset {offset}
                """
            )

            result = connection.execute(query)
            result = result.fetchall()
            
            result = replace_nan_on_list_tuple(result)
            result = replace_spaces_on_list_tuple(result)
            
            empty_df=pd.DataFrame(columns=columns)
            df_est=empty_df if len(result)==0 else pd.DataFrame(result, columns=columns)

            this_estab=tuple([estab[0] for estab in result])

            columns=[
                'cnpj_basico',
                'razao_social',
                'ente_federativo_responsavel',
                'porte_empresa',
                'capital_social',
                'natureza_juridica'
            ]
            columns_str=", ".join(columns)
            
            query = text(
                f"""
                    select
                        {columns_str}
                    from empresa
                    where cnpj_basico in {this_estab}
                """
            )
            
            result = connection.execute(query)
            result = result.fetchall()[0]
            
            df_comp=empty_df if len(result)==0 else pd.DataFrame(result, columns=columns)
            
            df=pd.merge(df_est, df_comp, on='cnpj_basico', how='left')
            
            return df
    
    def get_establishment(self, cnpj: CNPJ):
        with self.database.engine.begin() as connection:
            # Create the table if it does not exist
            query = text(
                f"""
                    select
                        distinct cnpj_basico, cnpj_ordem, cnpj_dv, correio_eletronico,
                        data_inicio_atividade,  data_situacao_cadastral, situacao_cadastral, 
                        motivo_situacao_cadastral, nome_fantasia, 
                        tipo_logradouro, logradouro, numero, complemento, bairro, municipio, cep, uf,
                        cnae_fiscal_principal, cnae_fiscal_secundaria, identificador_matriz_filial, 
                        situacao_especial, data_situacao_especial,
                        ddd_1, telefone_1, ddd_2, telefone_2
                    from estabelecimento est
                    where
                    est.cnpj_basico = '{cnpj.basico_int}' AND
                    est.cnpj_ordem = '{cnpj.ordem_int}' AND
                    est.cnpj_dv = '{cnpj.digitos_verificadores_int}'
                """
            )
            
            establishment_result = connection.execute(query)
            establishment_result = establishment_result.fetchall()
            
            establishment_result = replace_nan_on_list_tuple(establishment_result)
            establishment_result = replace_spaces_on_list_tuple(establishment_result)

            columns=[
                "cnpj_basico", "cnpj_ordem", "cnpj_dv", "email", "data_inicio_atividade",  
                "data_situacao_cadastral", "situacao_cadastral", "motivo_situacao_cadastral", "nome_fantasia", 
                "tipo_logradouro", "logradouro", "numero", "complemento", "bairro", "municipio", "cep", "uf",
                "cnae_fiscal_principal", "cnae_fiscal_secundaria", "identificador_matriz_filial", 
                "situacao_especial", "data_situacao_especial",
                "ddd_1", "telefone_1", "ddd_2", "telefone_2"
            ]
            empty_df=pd.DataFrame(columns=columns)
            df=empty_df if len(establishment_result)==0 else pd.DataFrame(establishment_result, columns=columns)
            
            return df

    def get_city(self, code: str):
        """
        Get the city for the code.
        
        Parameters:
        code (str): The code of the city.
        
        Returns:
        str: The name of the city.
        """
        with self.database.engine.begin() as connection:
            query=text(
                f"""
                    select
                        distinct descricao
                    from munic
                    where codigo = '{code}' 
                """
            )
            
            municipio_result = connection.execute(query)
            
            return None if not municipio_result else municipio_result.fetchall()[0][0]
    
    def get_cnaes(self, limit: int = 10):
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
                """
            )
            
            cnaes_result = connection.execute(query)
            cnaes_result = cnaes_result.fetchall()
            
            columns = ["codigo", "descricao"]
            
            return pd.DataFrame(cnaes_result, columns=columns) 

    def get_legal_natures(self, limit: int = 10):
        """
        Get all legal natures from the database.
        
        Returns:
        DataFrame: The DataFrame with the legal natures.
        """
        
        with self.database.engine.begin() as connection:
            query = text(
                f"""
                    select
                        codigo, descricao
                    from natju
                    limit {limit}
                """
            )
            
            legal_natures_result = connection.execute(query)
            legal_natures_result = legal_natures_result.fetchall()
            
            columns = ["codigo", "descricao"]
            
            return pd.DataFrame(legal_natures_result, columns=columns)

    def get_company(self, cnpj: CNPJ):
        """
        Get the company for the CNPJ.
        
        Parameters:
        cnpj (CNPJ): The CNPJ object.
        
        Returns:
        DataFrame: The DataFrame with the company.
        """
        
        with self.database.engine.begin() as connection:
            columns=[
                'cnpj_basico',
                'razao_social',
                'ente_federativo_responsavel',
                'porte_empresa',
                'capital_social',
                'natureza_juridica'
            ]
            columns_str=", ".join(columns)
            
            query=text(
                f"""
                with empresa_ as (
                    select
                        {columns_str}
                    from empresa emp
                        where emp.cnpj_basico = '{cnpj.basico_int}'
                )
                select
                    cnpj_basico,
                    razao_social,
                    ente_federativo_responsavel,
                    porte_empresa,
                    capital_social,
                    natju.descricao as natureza_juridica
                from empresa_ emp
                left join natju
                    on natju.codigo = emp.natureza_juridica
                """
            )

            company_result = connection.execute(query)
            company_result = company_result.fetchall()
            
            company_result = replace_nan_on_list_tuple(company_result)
            company_result = replace_spaces_on_list_tuple(company_result)

            empty_df=pd.DataFrame(columns=columns)
            df=empty_df if len(company_result)==0 else pd.DataFrame(company_result, columns=columns)
            
            return df

    def get_partners(self, cnpj: CNPJ):
        """
        Get the partners for the CNPJ.
        
        Parameters:
        cnpj (CNPJ): The CNPJ object.
        
        Returns:
        DataFrame: The DataFrame with the partners.
        """
        
        with self.database.engine.begin() as connection:
            query=text(
                f"""
                    with socios_ as (
                        select
                            cnpj_basico,
                            qualificacao_socio,
                            nome_socio_razao_social,
                            representante_legal,
                            pais
                        from socios
                        where cnpj_basico = '{cnpj.basico_int}'
                    )
                    SELECT 
                        cnpj_basico,
                        json_agg(
                            json_build_object(
                            'nome', nome_socio_razao_social,
                            'qual', qual_socio.descricao,
                            'pais_origem', pais,
                            'nome_rep_legal', representante_legal,
                            'qual_rep_legal', qual_representante.descricao
                            )
                        ) AS qsa
                    FROM socios_ soc
                    inner join quals qual_socio
                        on qual_socio.codigo = soc.qualificacao_socio
                    inner join quals qual_representante
                        on qual_representante.codigo = soc.qualificacao_socio
                    GROUP BY cnpj_basico
                """
            )
            
            partners_result = connection.execute(query)
            partners_result = partners_result.fetchall()
            
            partners_result = replace_nan_on_list_tuple(partners_result)
            partners_result = replace_spaces_on_list_tuple(partners_result)
            
            columns=[ 'cnpj_basico', 'qsa' ]
            partners_df=pd.DataFrame(partners_result, columns=columns).map(str)
            
            empty_df=pd.DataFrame(columns=columns)
            return empty_df if len(partners_df)==0 else pd.DataFrame(partners_df, columns=columns)

    def get_activities(self, cnpj: CNPJ):
        """
        Get the activities for the CNPJ.
        
        Parameters:
        cnpj (CNPJ): The CNPJ object.
        
        Returns:
        DataFrame: The DataFrame with the activities.
        """
        
        with self.database.engine.begin() as connection:
            query=text(
                f"""
                    with cnae_unnest as (
                        select
                            cnpj_basico,
                            unnest(string_to_array(est.cnae_fiscal_secundaria, ',')) AS codigo_cnae
                        FROM estabelecimento est
                        where cnpj_basico = '{cnpj.basico_int}'
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
                        on cast(cnae.codigo as text) = cast(cnae_unnest.codigo_cnae as text)
                        group by cnpj_basico, codigo, descricao
                        order by cnpj_basico, codigo, descricao
                    ),
                    atividade_principal as (
                        select
                            cnpj_basico,
                            json_agg(
                                json_build_object(
                                    'code', 
                                    CONCAT(
                                        SUBSTRING(cast(cnae.codigo as text), 1, 2), '.',
                                        SUBSTRING(cast(cnae.codigo as text), 3, 2), '-',
                                        SUBSTRING(cast(cnae.codigo as text), 5, 1), '-',
                                        SUBSTRING(cast(cnae.codigo as text), 7, 2)
                                    ),
                                    'text', cnae.descricao
                                )
                            ) as atividade_principal
                        from estabelecimento est
                        inner join cnae
                            on est.cnae_fiscal_principal = cnae.codigo::text
                        where cnpj_basico = '{cnpj.basico_int}'
                        group by cnpj_basico
                    ),
                    atividades_secundarias as (
                        select
                            cnpj_basico,
                            json_agg(
                                json_build_object(
                                    'code', 
                                    CONCAT(
                                        SUBSTRING(cast(codigo as text), 1, 2), '.',
                                        SUBSTRING(cast(codigo as text), 3, 2), '-',
                                        SUBSTRING(cast(codigo as text), 5, 1), '-',
                                        SUBSTRING(cast(codigo as text), 7, 2)
                                    ),
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
                    on cast(a_s.cnpj_basico as text) = cast(a_p.cnpj_basico as text)
                """
            )
        
            activities_result = connection.execute(query)
            activities_result = activities_result.fetchall()
            
            activities_result = replace_nan_on_list_tuple(activities_result)
            activities_result = replace_spaces_on_list_tuple(activities_result)
            
            columns=[
                'cnpj_basico',
                'atividade_principal',
                'atividades_secundarias'
            ]
            partners_df=pd.DataFrame(activities_result, columns=columns).map(str)
            
            empty_df=pd.DataFrame(columns=columns)
            return empty_df if len(partners_df)==0 else pd.DataFrame(partners_df, columns=columns)
    
    def get_cnpj_info(self, cnpj: CNPJ) -> Dict[str, str]:
        """
        Get the information for the CNPJ.
        
        Parameters:
        cnpj (CNPJ): The CNPJ object.
        
        Returns:
        dict: The dictionary with the CNPJ information.
        """
        # Get the establishment, partners, and company DataFrames
        establishment_df=self.get_establishment(cnpj)
        establishment_df['cnpj_basico']=establishment_df['cnpj_basico'].apply(int)

        # Check if the query returned any results
        codigo_municipio=establishment_df['municipio']

        if len(codigo_municipio) == 0:
            raise ValueError("Nenhum registro encontrado.")

        if len(codigo_municipio) > 1:
            raise ValueError(f"{len(codigo_municipio)} registros encontrados para CNPJ {cnpj}.")

        codigo_municipio=codigo_municipio[0]

        descricao_municipio=self.get_city(codigo_municipio)

        partners_df=self.get_partners(cnpj)
        partners_df['cnpj_basico']=partners_df['cnpj_basico'].apply(int)

        company_df=self.get_company(cnpj)
        company_df['cnpj_basico']=company_df['cnpj_basico'].apply(int)

        activities_df=self.get_activities(cnpj)
        activities_df['cnpj_basico']=activities_df['cnpj_basico'].apply(int)
    
        # Check if the query returned any results
        join_column='cnpj_basico'
        df_ = pd.merge(company_df, establishment_df, on=join_column, how='left')
        df_ = pd.merge(df_, partners_df, on=join_column, how='left') 
        df_ = pd.merge(df_, activities_df, on=join_column, how='left')
        
        entry=df_.to_dict('records')[0]

        columns=[
            'cnpj_basico',
            'data_inicio_atividade',
            'situacao_cadastral',
            'data_situacao_cadastral',
            'situacao_especial',
            'data_situacao_especial',
            'atividade_principal',
            'atividades_secundarias',
            'identificador_matriz_filial',
            'ente_federativo_responsavel',
            'razao_social',
            'nome_fantasia',
            'capital_social',
            'porte_empresa',
            'qsa',
            'logradouro',
            'numero',
            'complemento',
            'bairro',
            'cep',
            'municipio',
            'uf',
            'motivo_situacao_cadastral',
            'natureza_juridica',
            'email',
            'ddd_1',
            'telefone_1',
            'ddd_2',
            'telefone_2'
        ]

        cnpj_dict = dict()

        # Apply the formatting functions to the DataFrame
        cnpj_dict["abertura"] = format_database_date(entry["data_inicio_atividade"])

        # Situation
        situacao_dict={
            '1': 'NULA', '2': 'ATIVA', '3': 'SUSPENSA', '4': 'INAPTA', 8: 'BAIXADA'
        }
        cnpj_dict["situacao"] = situacao_dict[entry["situacao_cadastral"]]

        # Type
        tipo_dict={
            '1': 'MATRIZ', 
            '2': 'FILIAL' 
        }
        cnpj_dict['tipo'] = situacao_dict[entry["identificador_matriz_filial"]]
        cnpj_dict['nome'] = entry['razao_social']
        cnpj_dict['fantasia'] = entry['nome_fantasia']

        # Size
        porte_dict={
            '1': 'NÃO INFORMADO',
            '2': 'MICRO EMPRESA',
            '3': 'EMPRESA DE PEQUENO PORTE',
            '5': 'DEMAIS'
        }
        cnpj_dict['porte'] = porte_dict[str(entry["porte_empresa"])]
        
        # Nature
        cnpj_dict['natureza_juridica'] = entry['natureza_juridica']
        
        # Activities
        cnpj_dict['atividade_principal'] = entry['atividade_principal']
        cnpj_dict['atividades_secundarias'] = entry['atividades_secundarias']

        # Address
        cnpj_dict["logradouro"] = replace_spaces(entry["tipo_logradouro"]).strip()+\
                                ' '+replace_spaces(entry["logradouro"]).strip()
        cnpj_dict["numero"] = entry["numero"].strip()
        cnpj_dict["complemento"] = replace_spaces(entry["complemento"])
        cnpj_dict["bairro"] = replace_spaces(entry["bairro"])
        cnpj_dict["cep"] = format_cep(entry["cep"])
        cnpj_dict["municipio"] = descricao_municipio.strip()
        cnpj_dict["uf"] = entry["uf"].strip()

        # Email
        cnpj_dict["email"] = entry["email"]
        
        # Check if the DDD columns are invalid
        is_1_invalid = is_database_field_valid(entry["ddd_1"])
        is_2_invalid = is_database_field_valid(entry["ddd_2"])

        telefone_1 = "" if is_1_invalid else format_phone(entry["ddd_1"], entry["telefone_1"])
        telefone_2 = "" if is_2_invalid else format_phone(entry["ddd_2"], entry["telefone_2"]) 
        delimiter = " / " if telefone_1 and telefone_1 else ""
        cnpj_dict["telefone"] = telefone_1 + delimiter + telefone_2
        
        # Add the 'cnpj' and 'ultima_atualizacao' columns
        data_situacao_cadastral=entry["data_situacao_cadastral"]
        is_data_valid = is_database_field_valid(data_situacao_cadastral)
        cnpj_dict["data_situacao"] = format_database_date(data_situacao_cadastral) if is_data_valid else ''
        cnpj_dict["motivo_situacao"] = entry["motivo_situacao_cadastral"]
        
        # Special situation
        cnpj_dict["situacao_especial"] = entry["situacao_especial"]
        data_situacao_especial=entry["data_situacao_especial"]
        is_data_valid=is_database_field_valid(data_situacao_especial)
        cnpj_dict["data_situacao_especial"] = format_database_date(data_situacao_especial) if is_data_valid else '' 
        
        # Add the 'cnpj' and 'ultima_atualizacao' columns
        cnpj_dict["cnpj"] = cnpj.__str__()
        cnpj_dict["ultima_atualizacao"] = str(pd.Timestamp.now())

        # EFR
        cnpj_dict["efr"] = entry["ente_federativo_responsavel"]
        
        # Capital
        cnpj_dict["capital_social"] = entry["capital_social"]
        
        # Partners
        cnpj_dict["qsa"] = entry["qsa"]

        cnpj_dict["status"] = "OK"

        return cnpj_dict
