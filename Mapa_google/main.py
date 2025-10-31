from services.google_maps_client import GoogleMapsClient
import os
import time

def clear_screen():
    """Limpia la pantalla según el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")

def header():
    """Muestra un encabezado visual agradable."""
    print("=" * 60)
    print("             SISTEMA DE RUTAS DETALLADAS".center(60))
    print("=" * 60)
    print("Encuentra la ruta completa entre ciudades, con paradas intermedias.\n")
    print("Ejemplo de uso:")
    print("  - Ciudad de origen: Bogotá")
    print("  - Ciudad de destino: Ibagué")
    print("  - Paradas (opcional): Espinal, Melgar\n")
    print("-" * 60)

def main():
    clear_screen()
    header()

    API_KEY = "Digite su Api google cloud aqui para el uso del programa"   
    maps_client = GoogleMapsClient(API_KEY)

    # Entrada de datos
    origin = input("Ciudad de origen: ").strip()
    destination = input("Ciudad de destino: ").strip()
    stops_input = input("Paradas intermedias (separe con comas o deje vacío): ").strip()
    user_stops = [s.strip() for s in stops_input.split(",") if s.strip()] if stops_input else []

    # Confirmar datos antes de iniciar
    print("\n" + "-" * 60)
    print("Resumen de la solicitud:")
    print(f"  Origen:       {origin}")
    print(f"  Destino:      {destination}")
    if user_stops:
        print(f"  Paradas:      {', '.join(user_stops)}")
    else:
        print("  Paradas:      (ninguna)")
    print("-" * 60)
    input("Presione ENTER para calcular la ruta...")

    clear_screen()
    print("=" * 60)
    print("               CALCULANDO RUTA COMPLETA".center(60))
    print("=" * 60)
    time.sleep(0.5)

    try:
        # Construir lista completa de puntos a visitar
        travel_points = [origin] + user_stops + [destination]
        full_route = []
        total_distance = 0
        total_duration = 0

        # Calcular tramo por tramo
        for i in range(len(travel_points) - 1):
            segment = maps_client.get_detailed_route(travel_points[i], travel_points[i + 1])
            cities = segment["cities"]
            distance = segment["distance"]
            duration = segment["duration_hours"]

            # Evitar duplicados
            if full_route and cities[0].lower() == full_route[-1].lower():
                cities = cities[1:]

            full_route.extend(cities)
            total_distance += distance
            total_duration += duration

        # Limpiar repeticiones accidentales
        cleaned_route = []
        for city in full_route:
            if not cleaned_route or cleaned_route[-1].lower() != city.lower():
                cleaned_route.append(city)

        # Mostrar resultados
        print("\nRuta completa:")
        print("-" * 60)
        print(" -> ".join(cleaned_route))
        print("-" * 60)
        print(f"Distancia total aproximada: {total_distance:.2f} km")
        print(f"Duración total estimada: {total_duration:.2f} horas")

        # Enlace de Google Maps
        maps_url = "https://www.google.com/maps/dir/" + "/".join(
            city.replace(" ", "+") for city in cleaned_route
        )
        print("-" * 60)
        print("Ver ruta en Google Maps:")
        print(maps_url)
        print("=" * 60)

    except Exception as e:
        print("\nOcurrió un error al calcular la ruta:")
        print(f"{str(e)}")
        print("-" * 60)

if __name__ == "__main__":
    main()
