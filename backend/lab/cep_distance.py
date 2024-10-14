import math

import requests


def get_lat_lon_by_cep(cep):
    url = f"https://cep.awesomeapi.com.br/json/{cep}"
    response = requests.get(url)
    data = response.json()
    print(data)
    return float(data["lat"]), float(data["lng"])


def haversine_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6400.0

    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in kilometers
    distance = R * c
    return distance


def main(cep1, cep2):
    lat1, lon1 = get_lat_lon_by_cep(cep1)
    lat2, lon2 = get_lat_lon_by_cep(cep2)
    distance = haversine_distance(lat1, lon1, lat2, lon2)
    return distance


# Example usage
cep1 = "68980970"  # Replace with the first CEP
cep2 = "96255970"  # Replace with the second CEP

distance = main(cep1, cep2)
print(f"The distance between {cep1} and {cep2} is {distance:.2f} km.")
