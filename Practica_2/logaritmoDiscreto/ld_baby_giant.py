import math
from random import randint
import csv
import time
import psutil
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

def babyStepGiantStep(p, alpha, beta):
    n = math.ceil(math.sqrt(p))
    t = {}
    global MEMORY

    for r in range(n):
        t[pow(alpha, r, p)] = r
    
    alpha_inverso = pow(alpha, -n, p)
    gamma = beta
    for q in range(n):
        if gamma in t:
            j = t[gamma]
            k = q * n + j
            MEMORY = psutil.Process(os.getpid()).memory_info().rss  
            return k
        gamma = (gamma * alpha_inverso) % p

    MEMORY = psutil.Process(os.getpid()).memory_info().rss  
    return None

def main():
    global MEMORY
    resultadosList=[]
    listaTest = cargarCSV("logaritmoDiscretoSimp.csv")
    tiempos=[]
    memorys=[]
    i=0
    limit = 900
    resultadosList.append(["------------ Tamaño: 32 -----------"])
    resultadosList.append(["p", "alpha", "beta", "resultado", "tiempo", "memoria"])
    for fila in listaTest:
        if i==2: #Siguiente tamaño de pruebas
            mediaTiempo=doMedia(tiempos, 2)
            mediaMemory=doMedia(memorys, 2)
            resultadosList.append(["Media del tiempo: " + str(mediaTiempo)])
            resultadosList.append(["Media de la memoria: " + str((mediaMemory/(1024 ** 2)))])
            resultadosList.append(["------------ Tamaño: " + str(fila[0]) + " -----------"])
            resultadosList.append(["p", "alpha", "beta", "resultado", "tiempo", "memoria"])
            tiempos=[]
            memorys=[]
            i=0

            outputYuval = 'ldBabyGiantPruebaSimp.csv'
            with open(outputYuval, 'w', newline="") as file:
                csvwriter = csv.writer(file)
                csvwriter.writerows(resultadosList)

            print("Media del tiempo: " + str(mediaTiempo))
            print("Media de la memoria: " + str((mediaMemory/(1024 ** 2))))
            print("------------ Tamaño: " + str(fila[0]) + " -----------")

        tiempoInicio = time.time()
        resultado = babyStepGiantStep(int(fila[1]), int(fila[2]), int(fila[3]), limit)
        tiempo = time.time() - tiempoInicio
        memory = MEMORY
        if tiempo <= limit:
                tiempos.append(tiempo)
                memorys.append(memory)
                resultadosList.append([fila[1], fila[2], fila[3], resultado, tiempo, memory])
        else:
            resultadosList.append([fila[1], fila[2], fila[3], "--None--", tiempo, memory])
        
        if resultado is not None:
            print(str(fila[1]) + " - " + str(fila[2]) + " - " + str(fila[3]) + " - " + str(resultado) + " - " + str(tiempo) + " - " + str(memory))
        else:
            print("No se encontró un resultado.")
        i=i+1

if __name__ == '__main__':
    main()