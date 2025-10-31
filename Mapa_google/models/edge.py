class Edge:
    """
    Representa una conexión no dirigida entre dos nodos (ciudades).
    """
    def __init__(self, origin, destination, distance: float, duration: str):
        self.origin = origin
        self.destination = destination
        self.distance = distance
        self.duration = duration

    def __repr__(self):
        return f"Edge({self.origin.name} ↔ {self.destination.name}, {self.distance} km, {self.duration})"
