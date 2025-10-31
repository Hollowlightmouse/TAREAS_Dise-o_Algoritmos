from typing import Dict, List, Set, Optional
from .edge import Edge
from .node import Node

class Graph:
    """
    Representa un grafo no dirigido de ciudades y sus conexiones.
    """
    def __init__(self):
        self.nodes: Dict[str, Node] = {}

    def add_vertex(self, city_name: str) -> Node:
        if city_name not in self.nodes:
            self.nodes[city_name] = Node(city_name)
        return self.nodes[city_name]

    def add_edge(self, origin_name: str, destination_name: str, distance: float, duration: str) -> None:
        origin = self.add_vertex(origin_name)
        destination = self.add_vertex(destination_name)
        edge = Edge(origin, destination, distance, duration)

        origin.add_edge(edge)
        destination.add_edge(edge)  # No dirigido

    def find_shortest_path(self, origin: str, destination: str, visited: Optional[Set[str]] = None) -> Optional[List[Dict]]:
        """
        Encuentra el camino más corto entre dos ciudades usando búsqueda recursiva.
        """
        if visited is None:
            visited = set()

        if origin == destination:
            return []

        if origin not in self.nodes:
            return None

        visited.add(origin)
        shortest_path = None
        min_distance = float('inf')

        for edge in self.nodes[origin].edges:
            next_city = edge.destination.name if edge.origin.name == origin else edge.origin.name
            if next_city not in visited:
                path = self.find_shortest_path(next_city, destination, visited.copy())
                if path is not None:
                    total_distance = edge.distance + sum(seg["distance"] for seg in path)
                    if total_distance < min_distance:
                        min_distance = total_distance
                        shortest_path = [{"origin": origin, "destination": next_city, "distance": edge.distance, "duration": edge.duration}] + path
        return shortest_path

    def find_optimal_route(self, origin: str, destination: str, waypoints: List[str] = None) -> List[Dict]:
        """
        Encuentra la ruta óptima entre dos ciudades, con posibles paradas intermedias.
        """
        if not waypoints:
            return self.find_shortest_path(origin, destination)

        points = [origin] + waypoints + [destination]
        complete_route = []

        for i in range(len(points) - 1):
            segment = self.find_shortest_path(points[i], points[i + 1])
            if segment is None:
                raise Exception(f"No se pudo encontrar ruta entre {points[i]} y {points[i + 1]}")
            complete_route.extend(segment)
        return complete_route
