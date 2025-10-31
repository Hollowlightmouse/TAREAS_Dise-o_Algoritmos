import googlemaps
from typing import Dict, List

class GoogleMapsClient:
    """
    Cliente de Google Maps que obtiene rutas detalladas y ciudades intermedias.
    """
    def __init__(self, api_key: str):
        self.client = googlemaps.Client(key=api_key)

    def get_detailed_route(self, origin: str, destination: str) -> Dict:
        """
        Devuelve las ciudades intermedias reales, distancia total y duración total.
        """
        try:
            directions = self.client.directions(
                origin,
                destination,
                mode="driving",
                language="es"
            )

            if not directions:
                raise Exception(f"No se encontró una ruta entre {origin} y {destination}")

            route = directions[0]
            legs = route["legs"]

            cities = [origin]
            total_distance = 0
            total_duration = 0

            for leg in legs:
                total_distance += leg["distance"]["value"]
                total_duration += leg["duration"]["value"]

                # Buscar ciudades intermedias a partir de coordenadas
                for step in leg["steps"]:
                    location = step.get("end_location", {})
                    if location:
                        result = self.client.reverse_geocode(
                            (location.get("lat"), location.get("lng")),
                            language="es"
                        )
                        if result:
                            for comp in result[0]["address_components"]:
                                if "locality" in comp["types"]:
                                    city = comp["long_name"]
                                    if city not in cities:
                                        cities.append(city)
                                    break

            if destination not in cities:
                cities.append(destination)

            return {
                "cities": cities,
                "distance": total_distance / 1000,
                "duration_hours": total_duration / 3600
            }

        except Exception as e:
            raise Exception(f"Error al obtener la ruta detallada: {str(e)}")
