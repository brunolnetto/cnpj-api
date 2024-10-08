from collections import Counter
from typing import List

import nltk
from nltk.corpus import stopwords
from nltk.metrics import edit_distance

from backend.app.setup.logging import logger


def init_nltk():
    """
    This function initializes the NLTK library.
    """
    try:
        nltk.download("stopwords")
    except Exception as e:
        logger.error(f"Error downloading NLTK package 'stopwords': {e}")

    try:
        nltk.download("punkt")
    except Exception as e:
        logger.error(f"Error downloading NLTK package 'punkt': {e}")

    try:
        nltk.download("punkt_tab")
    except Exception as e:
        logger.error(f"Error downloading NLTK package 'punkt_tab': {e}")


def find_most_possible_tokens(
    eligible_tokens: List[str], token: str, limit_count: int
) -> List[str]:
    """
    This function finds the most possible city names from a list of eligible tokens based on a
    given token,
    using a combination of word overlap and Levenshtein distance.

    Args:
        eligible_tokens (list[str]): The list of eligible city names.
        token (str): The reference city name to compare with.
        limit_count (int): The number of most possible city names to return.

    Returns:
        list[str]: The list of the most possible city names.
    """
    # Preprocess data
    stop_words = stopwords.words("english")

    processed_tokens = [name.lower() for name in eligible_tokens]
    processed_municipality = token.lower()

    # Calculate word frequencies (optional, for combined scoring)
    word_freq_municipality = Counter()
    for word in nltk.word_tokenize(processed_municipality):
        if word not in stop_words:  # Exclude stop words
            word_freq_municipality[word] += 1

    # Score tokens based on combined factors
    scored_tokens = []
    for i, name in enumerate(processed_tokens):
        # Calculate Levenshtein distance
        lev_distance = edit_distance(name, processed_municipality)

        # Combine score (optional, adjust weights as needed)
        # You can experiment with different weights for word overlap and Levenshtein distance
        # based on your specific needs. Here, we use a simple average.
        # score =
        # (
        #   sum(word_freq_municipality.get(word, 0) for word in nltk.word_tokenize(name)) /
        #   len(name)) * 0.5 + (1 - lev_distance / len(name)) * 0.5
        score = (
            lev_distance
            + sum(
                word_freq_municipality.get(word, 0) for word in nltk.word_tokenize(name)
            )
        ) / 2

        scored_tokens.append((score, i))  # Store index instead of name

    # Sort and select top results based on index
    sorted_tokens = sorted(
        scored_tokens, key=lambda x: x[0]
    )  # Sort by ascending score (lower score is better)
    results = {(score, eligible_tokens[i]) for score, i in sorted_tokens[:limit_count]}
    results = sorted(results, key=lambda x: x[0])
    results = [name for score, name in results]
    return results
