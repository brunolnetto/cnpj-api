import pytest

import nltk

from backend.app.api.utils.ml import find_most_possible_tokens

def test_find_most_possible_tokens():
    user_names = ["New York City", "Los Angeles", "Springfield", "Smalltown"]
    user_municipality = "New York"
    limit_munic_count = 2
    expected= ["New York City", "Smalltown"]

    nltk.download('stopwords')
    nltk.download('punkt')

    most_possible_cities = find_most_possible_tokens(
        user_names, user_municipality, limit_munic_count
    )
    
    assert most_possible_cities == expected


    

