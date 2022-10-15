import math

import numpy as np
import random
import matplotlib.pyplot as plt
import statistics

# A: Cantidad de billetes de 50 disponibles
# B: Cantidad de billetes de 100 disponibles
# C: Cantidad de billetes de 200 disponibles
# D: Cantidad de billetes de 500 disponibles
# E: Cantidad de billetes de 1000 disponibles


A, B, C, D, E = 100, 50, 20, 10, 5
CANTIDAD_POBLACION_INICIAL = 5
PROBABILIDAD_MUTACION = 50
CANTIDDA_DE_VUELTAS = 5
MONTO_A_RETIRAR = 4150


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
    poblacion_inicial = []
    for i in range(1, CANTIDAD_POBLACION_INICIAL):
        Xa, Xb, Xc, Xd, Xe = generar_combinacion()
        poblacion_inicial.append((Xa, Xb, Xc, Xd, Xe))
    return poblacion_inicial


# print(generar_poblacion_inicial())

def calcular_aptitud(individuo, montoARetirar):
    (Xa, Xb, Xc, Xd, Xe) = individuo
    valor = Xa * 50 + Xb * 100 + Xc * 200 + Xd * 500 + Xe * 1000
    if (montoARetirar == valor):
        r = (montoARetirar // 50) - contar_billetes(individuo)
    else:
        r = abs(montoARetirar - valor) * -1
    return r


def contar_billetes(individuo):
    sum = 0
    for i in range(0, 4):
        sum += individuo[i]
    return sum


def calcular_aptitudes(individuos, montoARetirar):
    resultado = []
    for i in range(0, len(individuos) - 1):  # GIANCITO : Podrias quitarle el 0 y el -1 y te daria lo mismo
        apt = calcular_aptitud(individuos[i], montoARetirar)
        resultado.append({
            'individuo': individuos[i],
            'aptitud': apt
        })
    return resultado


def mejor_individuo(individuo1, individuo2, montoARetirar):
    apt1 = calcular_aptitud(individuo1, montoARetirar)
    apt2 = calcular_aptitud(individuo2, montoARetirar)
    if apt1 > apt2:
        individuo = individuo1
    else:
        individuo = individuo2
    return individuo


def torneo(individuos, montoARetirar):
    resultado = []
    for i in range(0, len(individuos)):
        if i == len(individuos) - 1:
            individuo = mejor_individuo(individuos[i], individuos[0], montoARetirar)
        else:
            individuo = mejor_individuo(individuos[i], individuos[i + 1], montoARetirar)
        resultado.append(individuo)
    return resultado


def seleccion(individuos, montoARetirar):
    individuos = torneo(individuos, montoARetirar)
    return individuos


# iteramos los seleccionados y hacemos cruza entre i e i+1
# =============================================================================
def cruzamiento(individuos):
    resultado = []
    for i in range(0, len(individuos), 2):
        resultado.append(cruzar(individuos[i], individuos[i + 1]))
        resultado.append(cruzar(individuos[i + 1], individuos[i]))
    return resultado


# =============================================================================


# cruza simple. Los primeros 3 los tomamos de B, y los ultimos 2 de A.
def cruzar(indA, indB):
    return (indB[0], indB[1], indB[2], indA[3], indA[4])
    # implementar cruza entre 2 individuos


def mutar(individuos):
    x = random.randint(0, len(individuos) - 1)
    individuo = individuos[x]
    pos = random.randint(0, len(individuo) - 1)
    listIndividuo = list(individuo)
    listIndividuo[pos] += 1  # ver de agregar -1 tmb
    individuo = tuple(listIndividuo)
    individuos[x] = individuo
    return individuos


# se activa siempre y se ejecuta dependiendo de una probabilidad
def ejecuta_mutacion():
    x = random.randint(0, 100);
    return x <= PROBABILIDAD_MUTACION


def mutacion(individuos):
    mutados = []
    if ejecuta_mutacion():
        print("Muto")
        mutados = mutar(individuos)
    else:
        mutados = individuos
    return mutados


def obtener_aptitud(individuo):
    return individuo.get('aptitud')


def es_apto(individuo):
    return obtener_aptitud(individuo) >= 0


# MAIN

individuos = generar_poblacion_inicial()
print("Poblacion inicial: ", individuos)
stop = False
i = 0

while i < CANTIDDA_DE_VUELTAS:
    seleccionados = seleccion(individuos, MONTO_A_RETIRAR)
    print("Seleccionados: ", individuos)
    individuosCruzados = cruzamiento(seleccionados)
    print("Cruzados:      ", individuosCruzados)
    individuosMutados = mutacion(individuosCruzados)
    print("Mutados:       ", individuosMutados)
    individuos = individuosMutados
    i = i + 1
