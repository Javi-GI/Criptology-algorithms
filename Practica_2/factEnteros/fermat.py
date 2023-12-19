import math
import psutil
from random import randint
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

def fermatAssert(n, limit):
    a = math.isqrt(n)
    b2 = a*a - n
    b = math.isqrt(n)
    count = 0
    tiempoInicio = time.time()
    cronometro = 0
    while b*b != b2 and cronometro < limit:
        #if verbose:
        #    print('Trying: a=%s b2=%s b=%s' % (a, b2, b))
        a = a + 1
        b2 = a*a - n
        b = math.isqrt(b2)
        count += 1
        cronometro = time.time() - tiempoInicio
    p=a+b
    q=a-b
    assert n == p * q
    #print('a=',a)
    #print('b=',b)
    #print('p=',p)
    #print('q=',q)
    #print('pq=',p*q)
    return p, q

def algoritmoFermat(n, limit):
    global MEMORY
    a = (math.trunc(math.sqrt(n)))+1
    b = pow(a,2) - n
    tiempoInicio = time.time()
    cronometro = 0
    while not math.sqrt(b).is_integer() or (((a - math.sqrt(b))*(a + math.sqrt(b)))-n) != 0 and cronometro < limit :
        a = a + 1
        b = pow(a,2) - n
        cronometro = time.time() - tiempoInicio
    MEMORY = psutil.Process(os.getpid()).memory_info().rss
    return  (a - math.sqrt(b), a + math.sqrt(b))

# MAIN
def main():
    global MEMORY
    resultadosList=[]
    #tamanios=[24,32,40,44,48,52,56,60,64,68,72,76,80,92,104]
    tamanios=[32,40,44,48,52,56,60,64,68,72,76,80,92]
    listaTest = cargarCSV("factorizarNumerosExt.csv")
    limit = 900
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
            resultado = fermatAssert(int(test[i]), limit) #ALGORITMO
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
        outputYuval = 'fermatPruebaExtAssert.csv'
        with open(outputYuval, 'w', newline="") as file:
            csvwriter = csv.writer(file)
            csvwriter.writerows(resultadosList)

if __name__ == '__main__':
    main()