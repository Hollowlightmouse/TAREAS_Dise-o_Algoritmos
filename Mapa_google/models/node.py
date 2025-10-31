class Node:
    """
    Representa una ciudad o punto en el grafo.
    """
    def __init__(self, name: str):
        self.name = name
        self.edges = []

    def add_edge(self, edge):
        if edge not in self.edges:
            self.edges.append(edge)

    def __repr__(self):
        return f"Node({self.name})"
