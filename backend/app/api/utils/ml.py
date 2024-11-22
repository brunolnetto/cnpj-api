from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

import nltk
from nltk.corpus import stopwords
from nltk.metrics import edit_distance

from backend.app.setup.logging import logger


def init_nltk() -> None:
    """Initializes NLTK by downloading necessary datasets."""
    try:
        nltk.download("stopwords", quiet=True)
        nltk.download("punkt", quiet=True)
        nltk.download("punkt_tab", quiet=True)
    except Exception as e:
        logger.error(f"Error downloading NLTK packages: {e}")


def compute_token_score(
    name: str, processed_municipality: str, word_freq_municipality: Counter
) -> tuple[float, str]:
    """Helper function to compute the score for each eligible token."""
    # Calculate the edit distance
    distance = edit_distance(name.lower(), processed_municipality)

    # Compute word frequency score
    word_score = sum(word_freq_municipality.get(word, 0)
                     for word in nltk.word_tokenize(name.lower())) / 2

    # Return combined score and token name
    return distance + word_score, name


def find_most_possible_tokens(
    eligible_tokens: List[str], token: str, limit_count: int
) -> List[str]:
    """
    Finds the most possible tokens from a list of eligible tokens based on a given token.

    Args:
        eligible_tokens (List[str]): The list of eligible tokens (e.g., city names).
        token (str): The reference token (e.g., city name) to compare with.
        limit_count (int): The number of most possible tokens to return.

    Returns:
        List[str]: The list of the most possible tokens.
    """
    stop_words = set(stopwords.words("english"))
    processed_municipality = token.lower()
    token_words = nltk.word_tokenize(processed_municipality)

    # Calculate word frequencies for the reference token
    word_freq_municipality = Counter(
        word for word in token_words if word not in stop_words
    )

    # Parallelize the scoring of tokens
    scored_tokens = []
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(
                compute_token_score, name, processed_municipality, word_freq_municipality
            )
            for name in eligible_tokens
        ]

        # Collect the results as they complete
        for future in as_completed(futures):
            scored_tokens.append(future.result())

    # Sort and select top results based on score
    results = sorted(scored_tokens, key=lambda x: x[0])[:limit_count]
    return [name for _, name in results]
