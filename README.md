# Algoritmos de Criptoanálisis

En este repositorio se encuentran diversos algoritmos desarrollados para la clase de Criptología y Seguridad de Datos durante mi Maestría. Los algoritmos están implementados en Python, utilizando la biblioteca Pandas para generar las tablas de resultados.

Puedes encontrar el análisis completo de los algoritmos en el archivo PDF dentro de este repositorio.

## Algoritmos de Factorización

- **Fermat**: Método basado en la diferencia de cuadrados. Su objetivo es expresar un número compuesto impar como la diferencia de dos cuadrados.
- **Pollard-Rho**: Algoritmo probabilístico utilizado para la factorización de enteros. Utiliza el algoritmo de detección de ciclos de Floyd para encontrar factores no triviales.
- **Pollard P-1**: Método de factorización de enteros que encuentra factores eligiendo valores aleatorios y computando sus potencias módulo el número a factorizar.
- **Lenstra**: Emplea curvas elípticas para encontrar factores no triviales de un número compuesto. Es especialmente efectivo para números con factores pequeños.

## Algoritmos de Logaritmo Discreto

- **Baby Step Giant Step**: Algoritmo para resolver problemas de logaritmo discreto. Utiliza un paso de precomputación para encontrar eficientemente el logaritmo en un grupo cíclico.
- **Pollard-Rho**: Este algoritmo se puede adaptar para encontrar logaritmos en grupos cíclicos, ofreciendo un enfoque probabilístico para resolver el problema del logaritmo discreto.
- **Pollard P-1**: Al igual que en la factorización, el algoritmo de Pollard P-1 se puede adaptar para resolver problemas de logaritmo discreto en grupos cíclicos con un orden conocido.
