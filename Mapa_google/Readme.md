# DOCUMENTACIÓN DEL DESARROLLO - SISTEMA DE RUTAS DETALLADAS

## Objetivo del Proyecto

Desarrollar un sistema modular en Python que calcule rutas detalladas entre ciudades utilizando la API de Google Maps, mostrando todas las ciudades intermedias necesarias para llegar desde un punto de origen hasta el destino final, con opción de incluir paradas intermedias personalizadas.

---


## Requisitos del Proyecto

### Librerías Necesarias
- `googlemaps` → Para interactuar con la API de Google Maps
- `os` y `time` → Para manejo de consola y temporización
- `typing` → Para anotaciones de tipos

Instalación:
`pip install googlemaps`


---

## Separación de Responsabilidades (Principios SOLID)

- **Single Responsibility Principle (S):**
  - Cada clase tiene una responsabilidad única.
  - `Node` modela una ciudad.
  - `Edge` representa una conexión.
  - `Graph` organiza las relaciones entre ciudades.
  - `GoogleMapsClient` gestiona la comunicación con la API de Google Maps.
  - `main.py` actúa como interfaz del usuario y coordina el flujo del programa.

- **Open/Closed Principle (O):**
  - Se puede ampliar la funcionalidad (por ejemplo, añadir pesos o tipos de conexión) sin modificar las clases base.

- **Dependency Inversion (D):**
  - El módulo principal (`main.py`) depende de abstracciones, no de implementaciones directas.

---

## Descripción de Archivos

### **main.py**
- Proporciona la interfaz de usuario en consola.
- Permite ingresar origen, destino y paradas opcionales.
- Coordina las llamadas al cliente de Google Maps.
- Muestra la ruta completa, distancia, duración y un enlace a Google Maps.
- Presenta una interfaz limpia, con títulos y secciones claras.

### **models/node.py**
- Define la estructura básica de un nodo (ciudad).
- Cada nodo puede tener varias conexiones asociadas.

### **models/edge.py**
- Define una arista no dirigida entre dos nodos.
- Contiene los datos de distancia y duración del trayecto.

### **models/graph.py**
- Gestiona los nodos y aristas del sistema.
- Implementa métodos para agregar ciudades, conectar rutas y buscar caminos.
- Permite calcular rutas óptimas entre ciudades utilizando distancias obtenidas desde la API.

### **services/google_maps_client.py**
- Contiene la clase `GoogleMapsClient`, encargada de comunicarse con la API de Google Maps.
- Métodos principales:
  - `get_detailed_route()`: obtiene la lista de ciudades intermedias, distancia y duración total.
- Utiliza **Geocoding inverso** para identificar los nombres de ciudades en cada tramo de la ruta.

---

## Ejecución del Programa

### 1. Configuración Inicial
Antes de ejecutar el sistema, se debe crear una **clave API de Google Maps**:
1. Acceder a [Google Cloud Console](https://console.cloud.google.com/).
2. Crear un proyecto y habilitar las siguientes APIs:
   - Directions API
   - Geocoding API
3. Generar una clave API y reemplazarla en el archivo `main.py`:
   ```python
   API_KEY = "Digite su Api google cloud aqui"
