# main.py
import os
import random
import math
from models.node import Node
from models.graph import Graph
from services.vrp_solver import VRPSolver
from services.google_maps_client import get_city_from_coords  # 🔹 nuevo import

def generate_random_nodes_around_bogota(n_customers=20, seed=42):
    """
    Genera nodos alrededor de Bogotá (lat ~ 4.7110, lon ~ -74.0721).
    Asigna ciudad/localidad real mediante reverse geocoding (API de Google Maps).
    """
    random.seed(seed)
    depot = Node(
        node_id=0,
        name="Almacén Bogotá",
        lat=4.7110,
        lon=-74.0721,
        demand=0,
        tw_start=0,
        tw_end=8 * 60,
        service_time=0,
    )

    customers = []
    for i in range(1, n_customers + 1):
        lat = 4.7110 + random.uniform(-0.18, 0.18)
        lon = -74.0721 + random.uniform(-0.2, 0.2)
        demand = random.randint(1, 5)
        tw_start = random.randint(0, 420)
        tw_end = tw_start + random.randint(60, 240)
        if tw_end > 8 * 60:
            tw_end = 8 * 60
        service_time = random.randint(5, 20)

        # 🔹 Obtener ciudad real con la API de Google Maps
        city = get_city_from_coords(lat, lon)

        cust = Node(
            node_id=i,
            name=f"Cliente {i} ({city})",
            lat=lat,
            lon=lon,
            demand=demand,
            tw_start=tw_start,
            tw_end=tw_end,
            service_time=service_time,
        )
        customers.append(cust)
    return depot, customers

def print_routes_console(depot, routes, graph, vehicle_count):
    """Imprime las rutas generadas en consola."""
    total_dist = 0.0
    total_load = 0
    print("\n=== RESUMEN DE RUTAS ===\n")
    for v in range(vehicle_count):
        if v < len(routes):
            r = routes[v]
            print(
                f"Vehículo {v+1} - Clientes: {len([s for s in r.stops if s != depot.id])} | "
                f"Carga: {r.load} | Distancia aprox: {r.distance_km:.2f} km | Duración aprox: {r.duration_min:.1f} min"
            )
            print(" Secuencia (depósito → ... → depósito):")
            for idx, node_id in enumerate(r.stops):
                node = graph.nodes[node_id]
                arrival = r.arrival_times[idx] if idx < len(r.arrival_times) else None
                if node_id == depot.id:
                    if idx == 0:
                        print(f"   [{idx}] DEPÓSITO (Salida) - {node.name}")
                    else:
                        print(f"   [{idx}] DEPÓSITO (Retorno) - {node.name}")
                else:
                    tw = f"[TW: {node.tw_start}-{node.tw_end}]"
                    arr_str = f"{arrival:.1f} min" if arrival is not None else "N/A"
                    print(
                        f"   [{idx}] {node.name} - Llegada: {arr_str} - "
                        f"Servicio: {node.service_time} min - Demanda: {node.demand} {tw}"
                    )
            print("-" * 60)
            total_dist += r.distance_km
            total_load += r.load
        else:
            print(f"Vehículo {v+1} - SIN ASIGNAR (sin ruta)")
            print("-" * 60)

    print("\n=== RESUMEN GLOBAL ===")
    print(f"Vehículos totales: {vehicle_count}")
    print(f"Rutas generadas: {len(routes)}")
    print(f"Distancia total estimada: {total_dist:.2f} km")
    print(f"Carga total entregada: {total_load}")
    print("\nNota: las ciudades se obtuvieron mediante la API de Google Maps.\n")

def main():
    NUM_CUSTOMERS = 20       # 🔹 límite de clientes
    VEHICLE_COUNT = 5
    VEHICLE_CAPACITY = 100

    print("🚚 Generando clientes aleatorios alrededor de Bogotá...\n")
    depot, customers = generate_random_nodes_around_bogota(NUM_CUSTOMERS, seed=123)

    graph = Graph()
    graph.add_node(depot)
    for c in customers:
        graph.add_node(c)

    print("\n⚙️ Construyendo matriz de distancias global...")
    graph.build_matrices()  # 🔹 se calcula solo una vez

    total_demand = sum(c.demand for c in customers)
    min_capacity_needed = math.ceil(total_demand / VEHICLE_COUNT)
    if VEHICLE_CAPACITY < min_capacity_needed:
        print(f"Ajustando capacidad por vehículo: {VEHICLE_CAPACITY} -> {min_capacity_needed}")
        VEHICLE_CAPACITY = min_capacity_needed

    solver = VRPSolver(
        graph=graph,
        depot_id=depot.id,
        vehicle_count=VEHICLE_COUNT,
        vehicle_capacity=VEHICLE_CAPACITY,
    )

    routes = solver.solve([c.id for c in customers])

    if len(routes) > VEHICLE_COUNT:
        print(f"Advertencia: se generaron {len(routes)} rutas, se mostrarán las primeras {VEHICLE_COUNT}.")
        routes = routes[:VEHICLE_COUNT]

    print_routes_console(depot, routes, graph, VEHICLE_COUNT)

if __name__ == "__main__":
    main()
