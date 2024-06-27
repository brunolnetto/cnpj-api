from typing import Dict, List, Union, Tuple

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
    else:
        return [cnpj[:8], cnpj[8:12], cnpj[12:14]]


def format_cnpj(cnpj_str: str) -> str:
    basico, ordem, digitos_verificadores = parse_cnpj_str(cnpj_str)

    basico = f"{basico[:2]}.{basico[2:5]}.{basico[5:8]}"
    ordem = f"{ordem}"
    digitos_verificadores = f"{digitos_verificadores}"

    return f"{basico}/{ordem}-{digitos_verificadores}"
