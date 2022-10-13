import numpy as np
import random
import matplotlib.pyplot as plt

# A: Cantidad de billetes de 50 disponibles
# B: Cantidad de billetes de 100 disponibles
# C: Cantidad de billetes de 200 disponibles
# D: Cantidad de billetes de 500 disponibles
# E: Cantidad de billetes de 1000 disponibles


A, B, C, D, E = 1000, 1000, 1000, 1000, 1000


# Xa: cantidad de billetes de 50 utilizados; Xa <= A
# Xb: cantidad de billetes de 100 utilizados; Xb <= B
# Xc: cantidad de billetes de 200 utilizados; Xc <= C
# Xd: cantidad de billetes de 500 utilizados; Xd <= D
# Xe: cantidad de billetes de 1000 utilizados; Xe <= E
# Y: salida, es la combinación de billetes a retirar.
# K: monto a retirar del cajero.

def generar_combinacion():
    Xa = random.randint(1, A)
    Xb = random.randint(1, B)
    Xc = random.randint(1, C)
    Xd = random.randint(1, D)
    Xe = random.randint(1, E)
    return Xa, Xb, Xc, Xd, Xe


def generar_poblacion_inicial():
    TAMAÑO_POBLACION_INICIAL = 500
    poblacion_inicial = []
    for i in range(1, TAMAÑO_POBLACION_INICIAL):
        Xa, Xb, Xc, Xd, Xe = generar_combinacion()
        poblacion_inicial.append((Xa, Xb, Xc, Xd, Xe))
    return poblacion_inicial


# print(generar_poblacion_inicial())

def calcular_aptitud(individuo, montoARetirar):
    billetes = obtener_billetes(individuo)
    valor = billetes[0] * 50 + billetes[1] * 100 + billetes[2] * 200 + billetes[3] * 500 + billetes[4] * 1000
    if montoARetirar == valor:
        r = (montoARetirar // 50) - contar_billetes(individuo)
    else:
        r = abs(K - N) * -1
    return r


def contar_billetes(individuo):
    sum = 0
    for i in range(0, 4):
        sum += individuo[i]
    return sum


def calcular_aptitudes(individuos, montoARetirar):
    resultado = []
    for i in range(0, len(individuos) - 1):
        apt = calcular_aptitud(individuos[i], montoARetirar)
        resultado.append({
            'billetes': individuos[i],
            'aptitud': apt
        })
    return resultado


def seleccion(individuos, montoARetirar):
    inviduos = calcular_aptitudes(individuos, montoARetirar)

    individuosIterator = filter(es_apto, individuos)  # removemos los que tienen aptitud -1
    individuos = list(individuosIterator)
    individuos.sort(key=obtener_aptitud, reverse=True)  # ordenamos de mejor a peor

    seleccionados = []
    # TODO: como sabemos cuantos tomar de los mejores?
    return individuos


# iteramos los seleccionados y hacemos cruza entre i e i+1, podriamos hacer un shuffle antes para hacer un cruzamiento mas random?
def cruzamiento(individuos):
    probabilidad_de_cruza = random.randint(1, 100)

    if probabilidad_de_cruza > 70:
        resultado = []
        for i in range(0, len(individuos) - 2):
            resultado.append(cruzar(individuos[i], individuos[i + 1]))
        return resultado
    else:
        return individuos


# cruza simple. Los primeros 3 los tomamos de B, y los ultimos 2 de A.
def cruzar(indA, indB):
    return (indB[0], indB[1], indB[2], indA[3], indA[4])
    # implementar cruza entre 2 individuos


def mutar(individuo):
    probabilidadDeMutacion = random.randint(1, 100)
    a, b, c, d, e = obtener_billetes(individuo)
    if probabilidadDeMutacion > 65:
        return {
            'billetes': (a, b, c, d, e),
            'aptitud': obtener_aptitud(individuo)
        }


def mutacion(individuos):
    mutados = []
    for i in range(0, len(individuos) - 1):
        mutados.append(mutar(individuos[i]))
    return mutados


def obtener_aptitud(individuo):
    return individuo.get('aptitud')


def obtener_billetes(individuo):
    return individuo.get('billetes')


def es_apto(individuo):
    return obtener_aptitud(individuo) >= 0


# MAIN

individuos = generar_poblacion_inicial()
cantidad_de_vueltas = 1000
i = 0
montoARetirar = 7350

while i < cantidad_de_vueltas:
    print("ejecutando linea", i)
    seleccionados = seleccion(individuos, montoARetirar)
    individuosCruzados = cruzamiento(seleccionados)
    individuosMutados = mutacion(individuosCruzados)
    individuos = individuosMutados
    i += 1

individuos.sort(key=obtener_aptitud, reverse=True)  # ordenamos de mejor a peor
print(individuos[0])



