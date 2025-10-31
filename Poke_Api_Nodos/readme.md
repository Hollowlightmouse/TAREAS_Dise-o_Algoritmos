# 📚 DOCUMENTACIÓN DEL DESARROLLO - POKEMON EVOLUTION SEARCH SYSTEM

## 🎯 Objetivo del Proyecto

Desarrollar un sistema que consuma la API de PokeAPI para construir y analizar grafos de evolución de Pokémon, implementando estructuras de datos (grafos) y algoritmos de búsqueda (búsqueda binaria).

---

## 🏗️ Arquitectura del Proyecto

### Estructura de Archivos
```
proyecto/
├──binary_search.py 
├──graph_builder.py
├──pokeapi_client
├── main.py         # Interfaz principal del usuario
└── DESARROLLO.md   # Este archivo de documentación
```

---

## 📋 Requisitos Cumplidos

### 1. Separación de Responsabilidades
- ✅ **pokelib.py**: Contiene todas las funciones de lógica y consumo de API
- ✅ **main.py**: Maneja la interfaz de usuario y el flujo del programa

### 2. Consumo de la PokeAPI
- ✅ Se utiliza la librería `requests` para hacer peticiones HTTP
- ✅ Endpoint utilizado: `https://pokeapi.co/api/v2/`
- ✅ Se navega a través de múltiples endpoints:
  - `/pokemon/{nombre}` → Información básica
  - `/pokemon-species/{id}` → Datos de especie
  - `/evolution-chain/{id}` → Cadena de evolución

### 3. Construcción Recursiva del Grafo
- ✅ Función `build_directed_graph()` implementada recursivamente
- ✅ Recorre la estructura JSON jerárquica (`chain` y `evolves_to`)
- ✅ Construye un diccionario como Lista de Adyacencia

### 4. Extracción y Ordenamiento de Nodos
- ✅ Función `extract_sorted_nodes()` extrae las claves del grafo
- ✅ Utiliza `sorted()` para ordenar alfabéticamente

### 5. Búsqueda Binaria Clásica
- ✅ Implementación iterativa con punteros `left` y `right`
- ✅ Complejidad temporal: O(log n)
- ✅ Retorna el índice si encuentra el elemento, -1 si no existe

---

## 🔧 Desarrollo Detallado por Función

### **pokelib.py**

#### 1. `get_evolution_chain(pokemon_name)`

**Propósito**: Obtener la cadena de evolución completa desde la API.

**Proceso**:
1. Consulta el endpoint `/pokemon/{nombre}` para obtener datos básicos
2. Extrae la URL de `species` del JSON recibido
3. Consulta el endpoint de species para obtener `evolution_chain`
4. Finalmente consulta el endpoint de la cadena de evolución
5. Retorna el JSON completo con toda la estructura evolutiva

**Manejo de errores**:
- Pokémon no encontrado (status 404)
- Errores de conexión
- Errores al procesar el JSON

**Código**:
```python
def get_evolution_chain(pokemon_name):
    # Obtiene la cadena de evolución completa de un Pokémon desde la PokeAPI
    try:
        # Paso 1: Obtener info del Pokémon
        pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
        pokemon_response = requests.get(pokemon_url)
        
        # Paso 2: Obtener URL de species
        species_url = pokemon_data['species']['url']
        
        # Paso 3: Obtener URL de evolution chain
        evolution_url = species_data['evolution_chain']['url']
        
        # Paso 4: Obtener datos de evolución
        return evolution_data
    except:
        return None
```

---

#### 2. `build_directed_graph(chain, graph=None)`

**Propósito**: Construir recursivamente un grafo dirigido desde la estructura JSON.

**Estructura del Grafo (Lista de Adyacencia)**:
```python
{
    'bulbasaur': ['ivysaur'],
    'ivysaur': ['venusaur'],
    'venusaur': []
}
```

**Algoritmo Recursivo**:
```
INICIO build_directed_graph(chain, graph)
    SI graph es None ENTONCES
        graph ← diccionario vacío
    FIN SI
    
    nombre_actual ← chain['species']['name']
    
    SI nombre_actual NO está en graph ENTONCES
        graph[nombre_actual] ← lista vacía
    FIN SI
    
    SI chain tiene 'evolves_to' Y no está vacío ENTONCES
        PARA CADA evolución EN chain['evolves_to'] HACER
            nombre_evolución ← evolución['species']['name']
            
            SI nombre_evolución NO está en graph[nombre_actual] ENTONCES
                Agregar nombre_evolución a graph[nombre_actual]
            FIN SI
            
            // ⬇️ RECURSIVIDAD ⬇️
            build_directed_graph(evolución, graph)
        FIN PARA
    FIN SI
    
    RETORNAR graph
FIN
```

**Ejemplo de Ejecución**:

Para la cadena: Bulbasaur → Ivysaur → Venusaur
```
Llamada 1: build_directed_graph({bulbasaur}, {})
  └─ Procesa: bulbasaur → ['ivysaur']
  └─ Llamada 2: build_directed_graph({ivysaur}, graph)
      └─ Procesa: ivysaur → ['venusaur']
      └─ Llamada 3: build_directed_graph({venusaur}, graph)
          └─ Procesa: venusaur → []
          └─ No hay más evoluciones → RETORNA
```

**Caso Base**: Cuando `evolves_to` está vacío (evolución final).

**Caso Recursivo**: Por cada evolución, se llama recursivamente la función.

**Código**:
```python
def build_directed_graph(chain, graph=None):
    # Construye recursivamente un grafo dirigido
    if graph is None:
        graph = {}
    
    current_name = chain['species']['name']
    
    if current_name not in graph:
        graph[current_name] = []
    
    # Procesar evoluciones recursivamente
    if 'evolves_to' in chain and chain['evolves_to']:
        for evolution in chain['evolves_to']:
            evolution_name = evolution['species']['name']
            graph[current_name].append(evolution_name)
            
            # ⬇️ AQUÍ ESTÁ LA RECURSIVIDAD ⬇️
            build_directed_graph(evolution, graph)
    
    return graph
```

---

#### 3. `extract_sorted_nodes(graph)`

**Propósito**: Extraer y ordenar los nombres de Pokémon del grafo.

**Proceso**:
1. Extrae todas las claves del diccionario con `list(graph.keys())`
2. Ordena alfabéticamente con `sorted()`
3. Retorna la lista ordenada

**Ejemplo**:
```python
# Grafo:
{'venusaur': [], 'bulbasaur': ['ivysaur'], 'ivysaur': ['venusaur']}

# Lista ordenada:
['bulbasaur', 'ivysaur', 'venusaur']
```

**Importancia**: Requisito para búsqueda binaria (necesita lista ordenada).

**Código**:
```python
def extract_sorted_nodes(graph):
    # Extrae y ordena los nombres de Pokémon
    nodes = list(graph.keys())
    return sorted(nodes)
```

---

#### 4. `binary_search(sorted_list, target)`

**Propósito**: Buscar un elemento en una lista ordenada con complejidad O(log n).

**Algoritmo Clásico**:
```
INICIO binary_search(lista_ordenada, objetivo)
    izquierda ← 0
    derecha ← longitud(lista_ordenada) - 1
    
    MIENTRAS izquierda ≤ derecha HACER
        medio ← (izquierda + derecha) DIV 2
        
        SI lista_ordenada[medio] = objetivo ENTONCES
            RETORNAR medio
        SINO SI lista_ordenada[medio] < objetivo ENTONCES
            izquierda ← medio + 1
        SINO
            derecha ← medio - 1
        FIN SI
    FIN MIENTRAS
    
    RETORNAR -1  // No encontrado
FIN
```

**Ejemplo de Ejecución**:

Buscar 'ivysaur' en ['bulbasaur', 'ivysaur', 'venusaur']:
```
Iteración 1:
  left=0, right=2, mid=1
  lista[1] = 'ivysaur' = target
  ✓ ENCONTRADO en índice 1
```

Buscar 'charmander' en ['bulbasaur', 'ivysaur', 'venusaur']:
```
Iteración 1:
  left=0, right=2, mid=1
  lista[1] = 'ivysaur' > 'charmander'
  right = 0

Iteración 2:
  left=0, right=0, mid=0
  lista[0] = 'bulbasaur' < 'charmander'
  left = 1

left > right → ✗ NO ENCONTRADO → retorna -1
```

**Código**:
```python
def binary_search(sorted_list, target):
    # Implementa búsqueda binaria
    left = 0
    right = len(sorted_list) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if sorted_list[mid] == target:
            return mid
        elif sorted_list[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

---

#### 5. `display_graph(graph)`

**Propósito**: Visualizar el grafo en formato legible.

**Salida de Ejemplo**:
```
=== EVOLUTION GRAPH (Adjacency List) ===
bulbasaur -> ivysaur
ivysaur -> venusaur
venusaur -> (does not evolve)
==========================================
```

---

## 🎮 Flujo de Ejecución del main.py

### Diagrama de Flujo
```
INICIO
  ↓
Solicitar nombre de Pokémon
  ↓
get_evolution_chain(pokemon_name)
  ↓
¿Datos obtenidos exitosamente?
  ├─ NO → Mostrar error y TERMINAR
  ↓
  └─ SÍ
     ↓
build_directed_graph(evolution_data['chain'])
  ↓
display_graph(graph)
  ↓
extract_sorted_nodes(graph)
  ↓
Mostrar nodos ordenados
  ↓
=== PRUEBAS DE BÚSQUEDA BINARIA ===
  ↓
Búsqueda 1: Pokémon que ESTÁ en el grafo
  ├─ binary_search(sorted_nodes, pokemon_1)
  └─ Mostrar resultado
  ↓
Búsqueda 2: Pokémon ingresado por usuario
  ├─ Solicitar nombre
  ├─ binary_search(sorted_nodes, pokemon_2)
  └─ Mostrar resultado
  ↓
Mostrar información detallada de evoluciones
  ↓
FIN
```

### Código del main.py
```python
from pokelib import (
    get_evolution_chain,
    build_directed_graph,
    extract_sorted_nodes,
    binary_search,
    display_graph
)

def main():
    # 1. Solicitar Pokémon
    pokemon_name = input("\nEnter Pokemon name: ").strip()
    
    # 2. Obtener datos de API
    evolution_data = get_evolution_chain(pokemon_name)
    
    # 3. Construir grafo
    graph = build_directed_graph(evolution_data['chain'])
    
    # 4. Mostrar grafo
    display_graph(graph)
    
    # 5. Ordenar nodos
    sorted_nodes = extract_sorted_nodes(graph)
    
    # 6. Búsquedas binarias
    result_1 = binary_search(sorted_nodes, sorted_nodes[1])
    result_2 = binary_search(sorted_nodes, "charmander")
```

---

## 📊 Complejidad Computacional

### Análisis de Complejidades

| Función | Complejidad Temporal | Complejidad Espacial |
|---------|---------------------|---------------------|
| `get_evolution_chain()` | O(1) - 3 peticiones HTTP constantes | O(n) - Tamaño del JSON |
| `build_directed_graph()` | O(n) - n = número de Pokémon en la cadena | O(n) - Almacena todos los nodos |
| `extract_sorted_nodes()` | O(n log n) - Debido a `sorted()` | O(n) - Copia de las claves |
| `binary_search()` | O(log n) - Búsqueda binaria clásica | O(1) - Solo variables |
| `display_graph()` | O(n + e) - n=nodos, e=aristas | O(1) - Solo imprime |

---

## 🧪 Casos de Prueba

### Caso 1: Cadena de Evolución Lineal
**Pokémon**: Bulbasaur

**Entrada**:
```
Enter Pokemon name: bulbasaur
```

**Grafo Esperado**:
```python
{
    'bulbasaur': ['ivysaur'],
    'ivysaur': ['venusaur'],
    'venusaur': []
}
```

**Búsqueda Binaria**:
- 'ivysaur' → ✓ Encontrado en índice 1
- 'charmander' → ✗ No encontrado

**Salida**:
```
=== EVOLUTION GRAPH (Adjacency List) ===
bulbasaur -> ivysaur
ivysaur -> venusaur
venusaur -> (does not evolve)
==========================================

Alphabetically sorted nodes: ['bulbasaur', 'ivysaur', 'venusaur']

Searching for 'ivysaur' in the graph...
✓ Found at index 1

Enter a Pokemon to search (e.g., charmander): charmander
✗ 'charmander' is not in this evolution chain
```

---

### Caso 2: Cadena con Ramificaciones
**Pokémon**: Eevee

**Grafo Esperado**:
```python
{
    'eevee': ['vaporeon', 'jolteon', 'flareon', 'espeon', 'umbreon', ...],
    'vaporeon': [],
    'jolteon': [],
    'flareon': [],
    ...
}
```

**Búsqueda Binaria**:
- 'flareon' → ✓ Encontrado
- 'pikachu' → ✗ No encontrado

---

### Caso 3: Pokémon que no Evoluciona
**Pokémon**: Lapras

**Grafo Esperado**:
```python
{
    'lapras': []
}
```

---

## 🔍 Conceptos Clave Implementados

### 1. Grafos Dirigidos
- **Definición**: Estructura de datos con nodos y aristas direccionales
- **Representación**: Lista de Adyacencia (diccionario de listas)
- **Aplicación**: Mapear evoluciones de Pokémon

**Ejemplo Visual**:
```
bulbasaur → ivysaur → venusaur
```

**Representación en Código**:
```python
{
    'bulbasaur': ['ivysaur'],
    'ivysaur': ['venusaur'],
    'venusaur': []
}
```

---

### 2. Recursividad
- **Definición**: Función que se llama a sí misma
- **Componentes**: 
  - **Caso base**: Condición de parada
  - **Caso recursivo**: Llamada a sí misma con parámetros diferentes
- **Aplicación**: Recorrer estructura jerárquica de evoluciones

**Ejemplo**:
```python
def build_directed_graph(chain, graph=None):
    # Caso base: No hay más evoluciones
    if not chain['evolves_to']:
        return graph
    
    # Caso recursivo: Procesar evoluciones
    for evolution in chain['evolves_to']:
        build_directed_graph(evolution, graph)  # Llamada recursiva
```

---

### 3. Búsqueda Binaria
- **Definición**: Algoritmo de búsqueda en listas ordenadas
- **Requisito**: La lista debe estar ordenada
- **Ventaja**: O(log n) vs O(n) de búsqueda lineal

**Comparación de Eficiencia**:
```
Lista de 1000 elementos:
- Búsqueda lineal: hasta 1000 comparaciones
- Búsqueda binaria: hasta 10 comparaciones
```

**Tabla de Comparaciones**:
| Tamaño Lista | Búsqueda Lineal | Búsqueda Binaria |
|--------------|----------------|------------------|
| 10           | 10             | 4                |
| 100          | 100            | 7                |
| 1,000        | 1,000          | 10               |
| 10,000       | 10,000         | 14               |

---

### 4. APIs RESTful
- **Definición**: Servicios web que responden con JSON
- **Método**: HTTP GET requests
- **Librería**: `requests` de Python

**Estructura de la API de PokeAPI**:
```
https://pokeapi.co/api/v2/
├── pokemon/{id or name}
├── pokemon-species/{id or name}
└── evolution-chain/{id}
```

---

## 🚀 Mejoras Futuras

1. **Caché de Resultados**: Guardar búsquedas previas para evitar consultas repetidas
```python
   cache = {}
   if pokemon_name in cache:
       return cache[pokemon_name]
```

2. **Visualización Gráfica**: Mostrar el grafo con `matplotlib` o `networkx`
```python
   import networkx as nx
   G = nx.DiGraph(graph)
   nx.draw(G, with_labels=True)
```

3. **Comparación de Cadenas**: Comparar evoluciones de múltiples Pokémon

4. **Información Adicional**: Mostrar nivel de evolución, métodos de evolución

5. **Interfaz Gráfica**: Implementar GUI con `tkinter` o `PyQt`

6. **Búsqueda por Tipo**: Filtrar Pokémon por tipo (fuego, agua, etc.)

7. **Estadísticas**: Mostrar estadísticas de evoluciones (HP, ataque, defensa)

---

## 💻 Instrucciones de Instalación y Uso

### Requisitos
- Python 3.7 o superior
- Librería `requests`

### Instalación
```bash
# 1. Instalar la librería requests
pip install requests

# 2. Descargar los archivos
# - pokelib.py
# - main.py
# - DESARROLLO.md

# 3. Ejecutar el programa
python main.py
```

### Ejemplo de Uso Completo
```bash
$ python main.py

==================================================
 POKEMON EVOLUTION SEARCH SYSTEM
==================================================

Enter Pokemon name: bulbasaur

Searching for information about 'bulbasaur'...

Building evolution graph...

=== EVOLUTION GRAPH (Adjacency List) ===
bulbasaur -> ivysaur
ivysaur -> venusaur
venusaur -> (does not evolve)
==========================================

Alphabetically sorted nodes: ['bulbasaur', 'ivysaur', 'venusaur']

==================================================
 BINARY SEARCH TEST
==================================================

Searching for 'ivysaur' in the graph...
✓ Found at index 1

Enter a Pokemon to search (e.g., charmander): charmander

Searching for 'charmander' in the graph...
✗ 'charmander' is not in this evolution chain

==================================================
 EVOLUTION INFORMATION
==================================================

Bulbasaur evolves to: Ivysaur

Ivysaur evolves to: Venusaur

Venusaur is the final evolution

==================================================
 END OF PROGRAM
==================================================
```

---

## 📝 Conclusiones

Este proyecto demuestra:
- ✅ Consumo efectivo de APIs REST
- ✅ Implementación de estructuras de datos (grafos)
- ✅ Algoritmos recursivos
- ✅ Algoritmos de búsqueda eficientes
- ✅ Buenas prácticas de programación (separación de responsabilidades)

### Conceptos Aprendidos:
1. **Manejo de JSON jerárquico**: Navegar estructuras anidadas
2. **Construcción recursiva de grafos**: Mapear relaciones complejas
3. **Búsqueda binaria iterativa**: Algoritmo eficiente O(log n)
4. **Organización modular de código**: Separación de lógica e interfaz
5. **Consumo de APIs**: Peticiones HTTP con requests

### Habilidades Desarrolladas:
- Pensamiento algorítmico
- Resolución de problemas
- Manejo de APIs externas
- Estructuras de datos avanzadas
- Programación funcional y recursiva

---

## 🐛 Solución de Problemas

### Error: "Pokemon not found"
**Causa**: Nombre de Pokémon incorrecto o no existe en la API

**Solución**: Verificar el nombre correcto en https://pokeapi.co/

---

### Error: "Connection error"
**Causa**: Sin conexión a internet o API caída

**Solución**: 
1. Verificar conexión a internet
2. Intentar más tarde
3. Verificar que https://pokeapi.co/ esté activa

---

### Error: "ModuleNotFoundError: No module named 'requests'"
**Causa**: Librería requests no instalada

**Solución**:
```bash
pip install requests
```

---

## 👨‍💻 Autor

Sistema desarrollado como ejercicio académico para aprender estructuras de datos y algoritmos aplicados a consumo de APIs.

**Tecnologías**: Python 3.x, requests, PokeAPI

**Fecha**: Octubre 2025

**Propósito**: Educativo - Aprendizaje de grafos, recursividad y búsqueda binaria

---

## 📖 Referencias

- [PokeAPI Documentation](https://pokeapi.co/docs/v2)
- [Python Requests Library](https://docs.python-requests.org/)
- [Binary Search Algorithm](https://en.wikipedia.org/wiki/Binary_search_algorithm)
- [Graph Data Structures](https://en.wikipedia.org/wiki/Graph_(abstract_data_type))
- [Recursion in Python](https://realpython.com/python-recursion/)
- [REST API Tutorial](https://restfulapi.net/)

---

## 📄 Licencia

Este proyecto es de código abierto para fines educativos.