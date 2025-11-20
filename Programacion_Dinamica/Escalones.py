def escalones(n):
    if n < 0:
        return []

 
    comb = [[] for _ in range(n + 1)]
    count = [0] * (n + 1)
    

    comb[0] = [[]] #Caso base
    count[0] = 1
    
    if n >= 1:
        comb[1] = [[1]]
        count[1] = 1
    if n >= 2:
        comb[2] = [[1, 1], [2]]
        count[2] = 2
    #Inicia desde i=3 hasta n
    for i in range(3, n + 1):
        lst = []
        for p in comb[i - 1]:
            lst.append(p + [1])
        for p in comb[i - 2]:
            lst.append(p + [2])
        for p in comb[i - 3]:
            lst.append(p + [3])
        comb[i] = lst
        count[i] = count[i - 1] + count[i - 2] + count[i - 3]
    
    return comb[n], count[n]
n=int(input("Ingrese cantidad de escalones: " ))
result_comb, result_count = escalones(n)
print("Cantidad de combinaciones para", n, "posibles escalones:", result_count)
print("Combinaciones para 4 escalones:", result_comb)