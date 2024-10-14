from typing import Dict, List, Union, Tuple

from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd

from backend.app.utils.misc import is_number


def calculate_cnpj_verification_digits(cnpj: str) -> Tuple[int, int]:
    """
    Calculates the verification digits of a given CNPJ number.

    Args:
        cnpj: The CNPJ number to calculate the verification digits for.

    Returns:
        The two verification digits.
    """
    if len(cnpj) != 14:
        raise ValueError("Invalid length. CNPJ should have 14 digits.")

    if not is_number(cnpj):
        raise ValueError("CNPJ contains non-numeric characters.")

    weights1 = "543298765432"
    weights2 = "6543298765432"
    sum1 = 0
    for i in range(1, 13):
        sum1 += int(cnpj[i - 1]) * int(weights1[i - 1])

    rest = sum1 % 11
    digit1 = 0 if rest < 2 else 11 - rest

    sum2 = 0
    for i in range(1, 14):
        sum2 += int(cnpj[i - 1]) * int(weights2[i - 1])

    rest = sum2 % 11
    digit2 = 0 if rest < 2 else 11 - rest

    return digit1, digit2


# Define the namedtuple for the CNPJ
def is_cnpj_str_valid(cnpj: str) -> Dict[str, Union[bool, str]]:
    """
    Validates a given CNPJ number.

    Args:
        cnpj: The CNPJ number to validate (string).

    Returns:
        True if the CNPJ is valid, False otherwise.
    """
    # Check length
    if len(cnpj) != 14:
        return {
            "is_valid": False,
            "reason": "Invalid length. CNPJ should have 14 digits.",
        }

    # Calculate verification digits
    try:
        digit1, digit2 = calculate_cnpj_verification_digits(cnpj)

    except ValueError:
        return {"is_valid": False, "reason": "CNPJ contains non-numeric characters."}

    # Check verification digits
    if cnpj[12] != str(digit1) or cnpj[13] != str(digit2):
        return {"is_valid": False, "reason": "Invalid verification digits."}

    # Valid CNPJ
    return {"is_valid": True, "reason": ""}


def are_cnpj_str_valid(cnpjs: List[str]):
    """
    Check if a list of CNPJ strings are valid.

    Args:
        cnpjs (List[str]): A list of CNPJ strings to be validated.

    Returns:
        List[bool]: A list of boolean values indicating whether each CNPJ string is valid or not.
    """
    return list(map(is_cnpj_str_valid, cnpjs))


def parse_cnpj_str(cnpj: str) -> List[str]:
    """
    Parses a CNPJ string by removing all non-numeric characters.

    Args:
        cnpj: The CNPJ string to parse.

    Returns:
        The parsed CNPJ string.
    """
    validation_dict = is_cnpj_str_valid(cnpj)

    if not validation_dict["is_valid"]:
        raise ValueError(validation_dict["reason"])

    return [cnpj[:8], cnpj[8:12], cnpj[12:14]]


def format_cnpj(cnpj_str: str) -> str:
    """
    Formats a CNPJ string.

    Args:
        cnpj_str (str): The CNPJ string to format.
    """

    basico, ordem, digitos_verificadores = parse_cnpj_str(cnpj_str)

    basico = f"{basico[:2]}.{basico[2:5]}.{basico[5:8]}"
    ordem = f"{ordem}"
    digitos_verificadores = f"{digitos_verificadores}"

    return f"{basico}/{ordem}-{digitos_verificadores}"


def format_cnpj_list(cnpj_list: List[str]) -> List[str]:
    """
    Formats a list of CNPJ strings.

    Args:
        cnpj_list (List[str]): The list of CNPJ strings to format.
    """
    cnpj_basicos = [f"'{str(cnpj_obj.basico_int)}'" for cnpj_obj in cnpj_list]
    return ",".join(cnpj_basicos)


async def get_cnpj_code_description_entries(session: AsyncSession, table_name: str):
    """
    Get all code-description entrie from the specified table.

    Args:
        table_name (str): The name of the table to query.
        limit (int, optional): The number of rows to fetch. Defaults to 10.
        offset (int, optional): The starting offset for the query. Defaults to 0.
        enable_pagination (bool, optional): Whether to enable pagination. Defaults to True.

    Returns:
        dict: A dictionary containing the CNAEs.
    """
    entries_result = await session.execute(
        text(f"SELECT codigo, descricao FROM {table_name}")
    )
    entries_result = entries_result.fetchall()

    entries_df = pd.DataFrame(entries_result, columns=["code", "text"])
    entries_dict = entries_df.to_dict(orient="records")

    return entries_dict
