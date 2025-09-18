import Lib

print("=== BÚSQUEDA DE PAÍSES DE EUROPA ===")
print("Lista disponible:")
print("paises =", Lib.paises)

continuar = "si"

while continuar == "si":
    pais = input("Ingrese el país que desea buscar (en inglés): ")

    print("")
    print("Seleccione el método de búsqueda:")
    print("1. Búsqueda Lineal")
    print("2. Búsqueda Binaria")

    opcion = input("Opción (1/2): ")

    if opcion == "1":
        resultado = Lib.busqueda_lineal(Lib.paises, pais)
    elif opcion == "2":
        resultado = Lib.busqueda_binaria(Lib.paises, pais)
    else:
        print("Opción inválida.")
        resultado = None

    if resultado:
        nombre, url = Lib.obtener_info_pais(resultado)
        if nombre and url:
            print("")
            print("País encontrado:", nombre)
            print("Google Maps:", url)
        else:
            print("")
            print("No se encontró información del país en la API.")
    else:
        print("")
        print("País no encontrado en la lista.")

    print("")
    continuar = input("¿Desea buscar otro país? (si/no): ")