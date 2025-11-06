# models/graph.py
from typing import Dict
from .node import Node
from services.google_maps_client import get_distance_and_duration

class Graph:
    """
    Grafo que obtiene distancias y tiempos de viaje reales desde la API de Google Maps.
    Calcula la matriz completa solo una vez, cuando se llama build_matrices().
    """

    def __init__(self):
        self.nodes: Dict[int, Node] = {}
        self.dist_matrix: Dict[int, Dict[int, float]] = {}
        self.time_matrix: Dict[int, Dict[int, float]] = {}

    def add_node(self, node: Node):
        """Agrega un nodo al grafo sin recalcular aún la matriz."""
        self.nodes[node.id] = node

    def build_matrices(self):
        """Calcula todas las distancias y tiempos (una sola vez)."""
        ids = list(self.nodes.keys())
        self.dist_matrix = {i: {} for i in ids}
        self.time_matrix = {i: {} for i in ids}

        print("\n🔄 Calculando matriz de distancias con Google Maps API... (solo una vez)")
        for i in ids:
            for j in ids:
                if i == j:
                    self.dist_matrix[i][j] = 0.0
                    self.time_matrix[i][j] = 0.0
                else:
                    n1 = self.nodes[i]
                    n2 = self.nodes[j]
                    d, t = get_distance_and_duration((n1.lat, n1.lon), (n2.lat, n2.lon))
                    self.dist_matrix[i][j] = d
                    self.time_matrix[i][j] = t
        print("✅ Matriz completa (distancias reales con Google Maps).")

    def distance(self, i: int, j: int) -> float:
        return self.dist_matrix[i][j]

    def travel_time(self, i: int, j: int) -> float:
        return self.time_matrix[i][j]
