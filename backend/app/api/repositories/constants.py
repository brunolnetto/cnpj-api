# Maps for the values of the fields in the database

# Company Size
SIZE_DICT = {
    "0": "NÃO INFORMADO",
    "1": "MICRO EMPRESA",
    "3": "EMPRESA DE PEQUENO PORTE",
    "5": "DEMAIS",
}

# Company Situation
SITUATION_DICT = {
    "1": "NULA",
    "2": "ATIVA",
    "3": "SUSPENSA",
    "4": "INAPTA",
    "8": "BAIXADA",
}

# Company Type
EST_TYPE_DICT = {"1": "MATRIZ", "2": "FILIAL"}


    def get_company_size_dict():
        """
        Get the company dictionary.

        Returns:
        - dict: The company dictionary.
        """
        return SIZE_DICT

    def get_establishment_type_dict():
        """
        Get the establishment type dictionary.

        Returns:
        - dict: The establishment type dictionary.
        """
        return EST_TYPE_DICT

    def get_company_situation_dict():
        """
        Get the company situation dictionary.

        Returns:
        - dict: The company situation dictionary.
        """
        return SITUATION_DICT