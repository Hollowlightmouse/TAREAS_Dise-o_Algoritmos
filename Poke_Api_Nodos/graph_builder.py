class GraphBuilder:
    
    @staticmethod
    def build_directed_graph(chain, graph=None):
        # Construye recursivamente un grafo dirigido (lista de adyacencia) recorriendo la estructura JSON jerárquica de evoluciones, mapeando cada Pokémon con sus evoluciones directas
        if graph is None:
            graph = {}
        
        current_name = chain['species']['name']
        
        if current_name not in graph:
            graph[current_name] = []
        
        if 'evolves_to' in chain and chain['evolves_to']:
            for evolution in chain['evolves_to']:
                evolution_name = evolution['species']['name']
                
                if evolution_name not in graph[current_name]:
                    graph[current_name].append(evolution_name)
                
                GraphBuilder.build_directed_graph(evolution, graph)
        
        return graph
    
    @staticmethod
    def extract_sorted_nodes(graph):
        # Extrae todas las claves (nombres de Pokémon) del grafo y las ordena alfabéticamente, retornando una lista ordenada para búsqueda binaria
        nodes = list(graph.keys())
        return sorted(nodes)
    
    @staticmethod
    def display_graph(graph):
        # Muestra visualmente el grafo de evolución en formato de lista de adyacencia para facilitar la comprensión de las relaciones evolutivas
        print("\n=== EVOLUTION GRAPH (Adjacency List) ===")
        for pokemon, evolutions in graph.items():
            if evolutions:
                print(f"{pokemon} -> {', '.join(evolutions)}")
            else:
                print(f"{pokemon} -> (does not evolve)")
        print("=" * 42)