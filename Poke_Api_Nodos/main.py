import pokeapi_client
import graph_builder
import binary_search

# Solicitar el nombre del Pokemon
pokemon_name = input("Enter Pokemon name: ")

# Obtener datos de la API
print("\nFetching data from PokeAPI...")
evolution_data = pokeapi_client.PokeAPIClient.get_evolution_chain(pokemon_name)

if evolution_data is None:
    print("Error: Could not get Pokemon data")
else:
    # Construir el grafo
    print("Building graph...")
    graph = graph_builder.GraphBuilder.build_directed_graph(evolution_data['chain'])
    
    # Mostrar el grafo
    graph_builder.GraphBuilder.display_graph(graph)
    
    # Extraer nodos ordenados
    sorted_nodes = graph_builder.GraphBuilder.extract_sorted_nodes(graph)
    print(f"\nSorted nodes: {sorted_nodes}")
    
    # Buscar un Pokemon en el grafo
    print("\n--- Binary Search Test ---")
    target2 = input("Enter a Pokemon to search: ")
    result2 = binary_search.BinarySearch.search(sorted_nodes, target2.lower())
    
    if result2 != -1:
        print(f"Found '{target2}' IS in the evolution chain (found at index {result2})")
    else:
        print(f"Not Found '{target2}' is NOT in the evolution chain")