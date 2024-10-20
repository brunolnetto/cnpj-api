from collections import Counter
from typing import List

import nltk
from nltk.corpus import stopwords
from nltk.metrics import edit_distance

from backend.app.setup.logging import logger


def init_nltk() -> None:
    """Initializes NLTK by downloading necessary datasets."""
    try:
        nltk.download("stopwords")
        nltk.download("punkt")
        nltk.download("punkt_tab")
    except Exception as e:
        logger.error(f"Error downloading NLTK packages: {e}")


def find_most_possible_tokens(
    eligible_tokens: List[str], token: str, limit_count: int
) -> List[str]:
    """
    Finds the most possible city names from a list of eligible tokens based on a given token.

    Args:
        eligible_tokens (List[str]): The list of eligible city names.
        token (str): The reference city name to compare with.
        limit_count (int): The number of most possible city names to return.

    Returns:
        List[str]: The list of the most possible city names.
    """
    stop_words = set(stopwords.words("english"))
    processed_municipality = token.lower()
    token_words = nltk.word_tokenize(processed_municipality)

    # Calculate word frequencies for the reference municipality
    word_freq_municipality = Counter(
        word for word in token_words if word not in stop_words
    )

    # Score tokens based on combined factors
    scored_tokens = [
        (
            edit_distance(name.lower(), processed_municipality)
            + sum(
                word_freq_municipality.get(word, 0)
                for word in nltk.word_tokenize(name.lower())
            )
            / 2,
            name,
        )
        for name in eligible_tokens
    ]

    # Sort and select top results based on score
    results = sorted(scored_tokens, key=lambda x: x[0])[:limit_count]
    return [name for _, name in results]
