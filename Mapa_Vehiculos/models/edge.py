# Models/edge.py
class Edge:
    def __init__(self, origin, destination, distance_km: float, duration_min: float):
        self.origin = origin
        self.destination = destination
        self.distance_km = distance_km
        self.duration_min = duration_min

    def __repr__(self):
        return f"Edge({self.origin.id}↔{self.destination.id}, {self.distance_km:.2f} km)"
