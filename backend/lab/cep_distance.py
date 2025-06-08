import math
import requests


def get_lat_lon_by_cep(cep):
    url = f"https://cep.awesomeapi.com.br/json/{cep}"
    response = requests.get(url)
    data = response.json()
    print(data)

    if "lat" not in data or "lng" not in data:
        raise ValueError(f"CEP {cep} inválido ou não encontrado.")

    return float(data["lat"]), float(data["lng"])


def haversine_distance(R, lat1, lon1, lat2, lon2):
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
    return R * c


def main(cep1, cep2):
    try:
        lat1, lon1 = get_lat_lon_by_cep(cep1)
        lat2, lon2 = get_lat_lon_by_cep(cep2)
    except ValueError as e:
        print(e)
        return None

    EARTH_RADIUS_KM = 6371.0
    return haversine_distance(EARTH_RADIUS_KM, lat1, lon1, lat2, lon2)


# Example usage
cep1_ = "75403728"
cep2_ = "75365529"

distance_ = main(cep1_, cep2_)
if distance_ is not None:
    print(f"The distance between {cep1_} and {cep2_} is {distance_:.2f} km.")
else:
    print("Distance could not be calculated due to invalid CEP.")
