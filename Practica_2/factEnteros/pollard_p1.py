import math
from random import randint
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

def algoritmoPollar_1(n, limit):
    global MEMORY

    a=randint(2, n-1)
    if 1 < math.gcd(a, n) < n:
        MEMORY = psutil.Process(os.getpid()).memory_info().rss
        return math.gcd(a,n)
    
    tiempoInicio = time.time()
    cronometro = 0
    k = 2
    while cronometro < limit:
        a = (pow(a,k))%n
        d = math.gcd(a-1,n)
        if(1 < d < n):
            MEMORY = psutil.Process(os.getpid()).memory_info().rss
            return d
        if(d == n):
            MEMORY = psutil.Process(os.getpid()).memory_info().rss
            return False
        k = k+1
        cronometro = time.time() - tiempoInicio
    return False

# MAIN
def main():
    global MEMORY
    resultadosList=[]
    #tamanios=[24,32,40,44,48,52,56,60,64,68,72,76,80,92,104]
    tamanios=[32,40,44,48,52,56,60,64]
    listaTest = cargarCSV("factorizarNumerosSimp.csv")
    limit = 300
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
            resultado = algoritmoPollar_1(int(test[i]), limit) #ALGORITMO
            tiempo = time.time() - tiempoInicio
            if tiempo <= limit and resultado != False:
                memory = MEMORY
                tiempos.append(tiempo)
                memorys.append(memory)
                resultadosList.append([int(test[i]), resultado, tiempo, memory])
                aciertos = aciertos + 1
            else:
                resultadosList.append([int(test[i]), "--None--", tiempo, memory])
            print("Número: ", int(test[i]) ," - Resultado: ", resultado, " - Tiempo: ", tiempo, " - Memoria: ", memory)
        if aciertos < 4:
            break
        
        mediaTiempo=doMedia(tiempos, aciertos)
        mediaMemory=doMedia(memorys, aciertos)
        resultadosList.append(["Media del tiempo: " + str(mediaTiempo)])
        resultadosList.append(["Media de la memoria: " + str((mediaMemory/(1024 ** 2)))])
        outputYuval = 'pollard_1_PruebaSimp1.csv'
        with open(outputYuval, 'w', newline="") as file:
            csvwriter = csv.writer(file)
            csvwriter.writerows(resultadosList)

if __name__ == '__main__':
    main()