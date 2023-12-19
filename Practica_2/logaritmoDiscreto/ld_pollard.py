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

def operacion(x, a, b, alpha, beta, p):
    
    x = (pow(alpha,a) * pow(beta,b)) % p
    switch_value = x % 3

    if switch_value == 1:
        x = (x*beta) % p
        a = a
        b = (b + 1) % (p-1)
    elif switch_value == 0:   
        x = (x*x) % p
        a = (2*a) % (p-1)
        b = (2*b) % (p-1)
    elif switch_value == 2:
        x = (x*alpha) % p
        a = (a + 1) % (p-1)
        b = b

    return x,a,b


def pollard_rho(p, alpha, beta, o, limit):
    global MEMORY
    a = b = aa = bb = 0
    i = x = xx = 1

    cronometro = 0
    tiempoInicio = time.time()

    while i < p and cronometro < limit:
        x,a,b = operacion(x, a, b, alpha, beta, p)
        xx,aa,bb = operacion(xx, aa, bb, alpha, beta, p)
        xx,aa,bb = operacion(xx, aa, bb, alpha, beta, p)

        if x == xx:
            if math.gcd(b - bb, o) != 1:
                MEMORY = psutil.Process(os.getpid()).memory_info().rss  
                return False
            MEMORY = psutil.Process(os.getpid()).memory_info().rss
            return ((aa - a) * pow(b - bb, -1, o)) % o
        i += 1
        cronometro = time.time() - tiempoInicio
    MEMORY = psutil.Process(os.getpid()).memory_info().rss
    return False

#POLLARD-RHO

def main():
    global MEMORY
    resultadosList=[]
    listaTest = cargarCSV("logaritmoDiscretoExt.csv")
    tiempos=[]
    memorys=[]
    i=0
    limit = 15
    resultadosList.append(["------------ Tamaño: 32 -----------"])
    resultadosList.append(["p", "alpha", "beta", "orden", "resultado", "tiempo", "memoria"])
    for fila in listaTest:
        if i==100:
            mediaTiempo=doMedia(tiempos, len(tiempos))
            mediaMemory=doMedia(memorys, len(memorys))
            resultadosList.append(["Media del tiempo: " + str(mediaTiempo)])
            resultadosList.append(["Media de la memoria: " + str((mediaMemory/(1024 ** 2)))])
            resultadosList.append(["------------ Tamaño: " + str(fila[0]) + " -----------"])
            resultadosList.append(["p", "alpha", "beta", "orden", "resultado", "tiempo", "memoria"])
            tiempos=[]
            memorys=[]
            i=0
        tiempoInicio = time.time()
        resultado = pollard_rho(int(fila[1]), int(fila[2]), int(fila[3]), int(fila[4]), limit)
        tiempo = time.time() - tiempoInicio
        memory = MEMORY
        if tiempo <= limit:
                tiempos.append(tiempo)
                memorys.append(memory)
                resultadosList.append([fila[1], fila[2], fila[3], fila[4], resultado, tiempo, memory])
        else:
            resultadosList.append([fila[1], fila[2], fila[3], fila[4], "--None--", tiempo, memory])
        
        if resultado is not False:
            print(f"El exponente k tal que β ≡ α^k (mod p) es: {resultado}. El tiempo es: {tiempo}")
        else:
            print("No se encontró un resultado.")
        i=i+1

    outputYuval = 'ldPollardPruebaExt.csv'
    with open(outputYuval, 'w', newline="") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerows(resultadosList)

if __name__ == '__main__':
    main()