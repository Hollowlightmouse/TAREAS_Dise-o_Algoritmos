def suma_digitos_mod(n): #Función recursiva para sumar los dígitos de un número
    
    if n <= 9:
        return n
    else:
        
        return (n % 10) + suma_digitos_mod(n // 10)
    
numero = int(input("Ingresa un numero entero positivo: "))
resultado = suma_digitos_mod(numero)
print(f"La suma de los dígitos de {numero} es: {resultado}")
