import requests
from math import radians, sin, cos, acos


def get_coordinates(address):
    api_url = "https://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": address
    }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    data = response.json()
    pos = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
    lon, lat = map(float, pos.split())
    return lon, lat


def find_nearest_pharmacy(center, radius=1000):
    api_url = "https://search-maps.yandex.ru/v1/"
    params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "text": "аптека",
        "ll": f"{center[0]},{center[1]}",
        "spn": "0.01,0.01",
        "type": "biz",
        "results": 1,
        "radius": radius
    }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    data = response.json()

    if "features" in data and len(data["features"]) > 0:
        pharmacy = data["features"][0]
        name = pharmacy["properties"]["CompanyMetaData"]["name"]
        address = pharmacy["properties"]["CompanyMetaData"]["address"]
        hours = pharmacy["properties"]["CompanyMetaData"].get("Hours", {}).get("text", "Время работы не указано")
        coords = list(map(float, pharmacy["geometry"]["coordinates"]))
        return {
            "name": name,
            "address": address,
            "hours": hours,
            "coords": coords
        }
    return None


def calculate_distance(lon1, lat1, lon2, lat2):
    earth_radius = 6371000
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    distance = earth_radius * acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon2 - lon1))
    return distance


def get_map_image(points, map_type="map"):
    api_url = "https://static-maps.yandex.ru/1.x/"
    pt = "~".join([f"{point['lon']},{point['lat']},pm2{point['icon']}" for point in points])
    params = {
        "l": map_type,
        "pt": pt
    }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    return response.content
