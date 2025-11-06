# Models/node.py
from typing import Optional

class Node:
    """
    Nodo representando el almacén o una entrega.
    Coordenadas en lat/lon, demanda (volumen), ventana de tiempo [tw_start, tw_end] en minutos,
    tiempo de servicio en minutos, y un id.
    """
    def __init__(self, node_id: int, name: str, lat: float, lon: float,
                 demand: int = 1,
                 tw_start: int = 0, tw_end: int = 8*60,  # minutos desde inicio del día laboral (8h -> 480)
                 service_time: int = 10):
        self.id = node_id
        self.name = name
        self.lat = lat
        self.lon = lon
        self.demand = demand
        self.tw_start = tw_start
        self.tw_end = tw_end
        self.service_time = service_time

    def __repr__(self):
        return f"Node({self.id}, {self.name}, demand={self.demand})"
