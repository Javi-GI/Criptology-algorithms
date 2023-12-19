from random import randint
import math
import psutil
import csv
import time
import os
MEMORY=0

def cargarCSV(ficherito):
    textoCargado = []
    with open(ficherito, newline='') as csvfile:
        texto = csv.reader(csvfile, delimiter=',')

        for row in texto:
            textoCargado.append(row)
    
    return textoCargado

def doMedia(resultados, div):
    suma = 0.0
    for x in range(0, div):
        suma = suma + resultados[x]
    media = suma/div
    return media


# Devuelve el inverso, y el MCD
def modular_inv(a, b):
    if b == 0:
        return 1, 0, a
    q, r = divmod(a, b)
    x, y, g = modular_inv(b, r)
    return y, x - q * y, g

def suma_eliptica(p, q, a, b, m):
    # Si el punto es infinito devuleve el otro
    if p[2] == 0: return q
    if q[2] == 0: return p
    if p[0] == q[0]: # Recta tangente a un punto
        if (p[1] + q[1]) % m == 0:
            return 0, 1, 0  # Infinity
        num = (3 * pow(p[0],2) + a) % m
        denom = (2 * p[1]) % m
    else: # Secante a dos puntos
        num = (q[1] - p[1]) % m
        denom = (q[0] - p[0]) % m
    inv, _, g = modular_inv(denom, m)

    # Arithmetic breaks. Imposible encontrar inverso
    if g > 1:
        #print("OCURRIO")
        return 0, 0, denom  # Failure
    
    x = (pow((num * inv),2) - p[0] - q[0]) % m # Xr = m^2 -xp -yq
    y = ((num * inv) * (p[0] - x) - p[1]) % m # Yr
    return x, y, 1 


# Multiplicacion (repeated addition and doubling) la forma más eficiente de multiplicación escalar
def multi_eliptica(k, p, a, b, m):
    r = (0, 1, 0)  # Infinito
    while k > 0:
        # Si el flag p esta activo devolver
        if p[2] > 1:
            return p
        if k % 2 == 1: # Si el numero es impar, indica que en binario acabaria en 1 con lo cual se realiza la operacion. Si es cero no se hace
            r = suma_eliptica(p, r, a, b, m)
        k = k // 2
        #print(k)
        p = suma_eliptica(p, p, a, b, m)
        #print(p)
    return r 

#def binari_mode(k, p, a, b, m):
    k = bin(k)[2:]
    r = (0, 1, 0)  # Infinito
    for i in range(len(k)):
        p = suma_eliptica(p, p, a, b, m)
    return p

#----------- Algoritmo de Lenstra -------------
def lenstra(n, limit, timeout):
    global MEMORY
    cronometro = 0
    tiempoInicio = time.time()

    while cronometro < timeout:
        #----- Generar una curva sin anomalias y un punto --------
        mcd = n
        while mcd == n:
            p = randint(0, n - 1), randint(0, n - 1),1
            a = randint(0, n - 1)
            b = (pow(p[1],2) - pow(p[0],3) - a * p[0]) % n
            mcd = math.gcd(4 * pow(a,3) + 27 * pow(b,2), n)  # Comprobar existencia de discontinuidades

        # Si tenemos mucha suerte podemos obtener resultado directo
        # Esto no tengo muy claro el porque, pero se puede quitar sin problemas
        if mcd > 1:
            MEMORY = psutil.Process(os.getpid()).memory_info().rss
            return mcd
        
        k = 2
        while k < limit:
            p = multi_eliptica(k, p, a, b, n)
            # Elliptic arithmetic breaks
            if p[2] > 1:
                #print("Resultado: ", p[2], " siendo el mcd(", p[2], ",", n, "): ")
                MEMORY = psutil.Process(os.getpid()).memory_info().rss
                return math.gcd(p[2], n)
            #print(k, " ----------- ", p)
            k = k + 1
        cronometro = time.time() - tiempoInicio
        
    MEMORY = psutil.Process(os.getpid()).memory_info().rss
    return False


# MAIN
def main():
    global MEMORY
    resultadosList=[]
    tamanios=[24,32,40,44,48,52,56,60,64,68,72,76,80,92,104]
    #tamanios=[32,40,44,48,52,56,60,64]
    listaTest = cargarCSV("factorizarNumerosExt.csv")
    limit = 5000
    timeout = 600
    for tam in range(len(tamanios)):
        tiempos=[]
        memorys=[]
        test = listaTest[tam]
        resultadosList.append(["------------ Tamaño: " + str(tamanios[tam]) + " -----------"])
        resultadosList.append(["Numero", "Resultado", "Tiempo", "Memoria"])
        print("------------ Tamaño: ", tamanios[tam], " -----------")
        aciertos = 0
        for i in range(len(test)):
            tiempoInicio = time.time()
            resultado = lenstra(int(test[i]), limit, timeout) #ALGORITMO
            tiempo = time.time() - tiempoInicio
            if resultado != False:
                memory = MEMORY
                tiempos.append(tiempo)
                memorys.append(memory)
                resultadosList.append([int(test[i]), resultado, tiempo, memory])
                aciertos = aciertos + 1
            else:
                resultadosList.append([int(test[i]), "--None--", tiempo, memory])
            print("Número: ", int(test[i]) ," - Resultado: ", resultado, " - Tiempo: ", tiempo, " - Memoria: ", memory)
        if aciertos < 50:
            break
        
        mediaTiempo=doMedia(tiempos, aciertos)
        mediaMemory=doMedia(memorys, aciertos)
        resultadosList.append(["Media del tiempo: " + str(mediaTiempo)])
        resultadosList.append(["Media de la memoria: " + str((mediaMemory/(1024 ** 2)))])
        outputYuval = 'lenstraPruebaExt.csv'
        with open(outputYuval, 'w', newline="") as file:
            csvwriter = csv.writer(file)
            csvwriter.writerows(resultadosList)

if __name__ == '__main__':
    main()
