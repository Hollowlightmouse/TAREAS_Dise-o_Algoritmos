# services/google_maps_client.py
import os
import requests
import json
import time

API_KEY = "Ingrese su API google cloud aqui"
CACHE_FILE = "distance_cache.json"
# Cargar cache previa si existe
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        CACHE = json.load(f)
else:
    CACHE = {}

def save_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(CACHE, f, ensure_ascii=False, indent=2)

def get_distance_and_duration(origin, destination, mode="driving"):
    """
    Obtiene distancia (km) y duración (min) entre dos coordenadas
    usando Google Maps Directions API.
    """
    if not API_KEY:
        raise RuntimeError("No se encontró GOOGLE_MAPS_API_KEY. Configura la variable de entorno.")

    orig_str = f"{origin[0]},{origin[1]}"
    dest_str = f"{destination[0]},{destination[1]}"
    cache_key = f"{orig_str}->{dest_str}"

    if cache_key in CACHE:
        return CACHE[cache_key]

    url = (
        f"https://maps.googleapis.com/maps/api/directions/json?"
        f"origin={orig_str}&destination={dest_str}&mode={mode}&key={API_KEY}"
    )

    resp = requests.get(url)
    if resp.status_code != 200:
        raise RuntimeError(f"Error al llamar a Google Maps API: {resp.status_code} - {resp.text}")

    data = resp.json()

    if data["status"] != "OK":
        raise RuntimeError(f"Google Maps API error: {data.get('status')} - {data.get('error_message')}")

    leg = data["routes"][0]["legs"][0]
    distance_km = leg["distance"]["value"] / 1000.0
    duration_min = leg["duration"]["value"] / 60.0

    CACHE[cache_key] = (distance_km, duration_min)
    save_cache()
    # Dormir brevemente para no saturar API
    time.sleep(0.1)
    return distance_km, duration_min
def get_city_from_coords(lat, lon):
    """
    Devuelve el nombre de la ciudad/localidad usando la API de Google Maps (Reverse Geocoding).
    Si falla o no se encuentra, devuelve 'Desconocido'.
    """
    if not API_KEY:
        return "Desconocido"

    cache_key = f"city:{lat:.4f},{lon:.4f}"
    if cache_key in CACHE:
        return CACHE[cache_key]

    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={API_KEY}"
    resp = requests.get(url)
    if resp.status_code != 200:
        return "Desconocido"

    data = resp.json()
    if data.get("status") != "OK":
        return "Desconocido"

    # Buscar el componente "locality" o "administrative_area_level_2"
    city = "Desconocido"
    results = data.get("results", [])
    if results:
        components = results[0].get("address_components", [])
        for comp in components:
            if "locality" in comp["types"] or "administrative_area_level_2" in comp["types"]:
                city = comp["long_name"]
                break

    CACHE[cache_key] = city
    save_cache()
    return city
