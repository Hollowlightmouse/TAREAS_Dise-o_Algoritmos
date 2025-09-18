import requests

# Lista de países de Europa (en inglés y ordenados alfabéticamente para búsqueda binaria)
paises = [
    "Austria", "Belgium", "Denmark", "Finland", "France",
    "Germany", "Ireland", "Italy", "Netherlands", "Norway",
    "Portugal", "Spain", "Sweden", "Switzerland", "United Kingdom"
]

# --- FUNCIONES DE BÚSQUEDA ---

def busqueda_lineal(lista, objetivo):
    # Normaliza el objetivo: elimina espacios y lo convierte a minúsculas
    objetivo = objetivo.strip().lower()
    # Recorre cada país en la lista
    for pais in lista:
        # Compara el país actual con el objetivo (ignorando mayúsculas/minúsculas)
        if pais.lower() == objetivo:
            return pais  # Retorna el país si lo encuentra
    return None  # Retorna None si no encuentra el país

def busqueda_binaria(lista, objetivo):
    # Normaliza el objetivo: elimina espacios y lo convierte a minúsculas
    objetivo = objetivo.strip().lower()
    izquierda = 0  # Índice inicial
    derecha = len(lista) - 1  # Índice final

    # Mientras el rango de búsqueda sea válido
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2  # Calcula el índice del medio
        # Compara el país en la posición media con el objetivo
        if lista[medio].lower() == objetivo:
            return lista[medio]  # Retorna el país si lo encuentra
        elif lista[medio].lower() < objetivo:
            izquierda = medio + 1  # Busca en la mitad derecha
        else:
            derecha = medio - 1  # Busca en la mitad izquierda
    return None  # Retorna None si no encuentra el país

# --- FUNCIÓN PARA CONSULTAR API ---
def obtener_info_pais(nombre_pais):
    url = "https://restcountries.com/v3.1/region/europe"
    try:
        # Realiza la petición HTTP a la API con un timeout de 10 segundos
        response = requests.get(url, timeout=10)
    except requests.RequestException:
        # Si ocurre un error en la petición, retorna None, None
        return None, None

    # Si la respuesta no es exitosa, retorna None, None
    if response.status_code != 200:
        return None, None

    # Convierte la respuesta en formato JSON
    data = response.json()

    # Recorre cada país en la respuesta de la API
    for pais in data:
        nombre = pais["name"]["common"]  # Obtiene el nombre común del país

        # Compara el nombre del país con el nombre buscado (ignorando mayúsculas/minúsculas)
        if nombre.lower() == nombre_pais.strip().lower():
            maps_url = pais["maps"]["googleMaps"]  # Obtiene el enlace de Google Maps
            return nombre, maps_url  # Retorna el nombre y el enlace

    return None, None  # Retorna None, None si no encuentra
