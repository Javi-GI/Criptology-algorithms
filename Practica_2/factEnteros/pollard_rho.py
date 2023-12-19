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

def algoritmoPollar(n, limit):
    global MEMORY
    a=b=randint(2, n-1)
    tiempoInicio = time.time()
    cronometro = 0
    while cronometro < limit :
        a = (pow(a,2) + 1)%n
        b = (pow(b,2) + 1)%n
        b = (pow(b,2) + 1)%n
        p = math.gcd(a-b, n)
        if(p > 1 and p < n):
            MEMORY = psutil.Process(os.getpid()).memory_info().rss
            return p
        if(p == n):
            MEMORY = psutil.Process(os.getpid()).memory_info().rss
            return n
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
            resultado = algoritmoPollar(int(test[i]), limit) #ALGORITMO
            tiempo = time.time() - tiempoInicio
            if tiempo <= limit:
                memory = MEMORY
                tiempos.append(tiempo)
                memorys.append(memory)
                resultadosList.append([int(test[i]), resultado, tiempo, memory])
                aciertos = aciertos + 1
            else:
                resultadosList.append([int(test[i]), "--None--", tiempo, memory])
            print("Número: ", int(test[i]) ," - Resultado: ", resultado, " - Tiempo: ", tiempo, " - Memoria: ", memory)
        
        mediaTiempo=doMedia(tiempos, aciertos)
        mediaMemory=doMedia(memorys, aciertos)
        resultadosList.append(["Media del tiempo: " + str(mediaTiempo)])
        resultadosList.append(["Media de la memoria: " + str((mediaMemory/(1024 ** 2)))])
        outputYuval = 'pollardRhoPruebaSimp1.csv'
        with open(outputYuval, 'w', newline="") as file:
            csvwriter = csv.writer(file)
            csvwriter.writerows(resultadosList)

if __name__ == '__main__':
    main()