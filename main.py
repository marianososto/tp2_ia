import math

import numpy as np
import random
import matplotlib.pyplot as plt
import statistics

# import graph

# A: Cantidad de billetes de 50 disponibles
# B: Cantidad de billetes de 100 disponibles
# C: Cantidad de billetes de 200 disponibles
# D: Cantidad de billetes de 500 disponibles
# E: Cantidad de billetes de 1000 disponibles


A, B, C, D, E = 1000, 500, 250, 100, 50  # esto nos da en total $250K
TOTAL_COMBINACIONES_POSIBLES = A * B * C * D * E
PROBABILIDAD_MUTACION = 50


# Xa: cantidad de billetes de 50 utilizados; Xa <= A
# Xb: cantidad de billetes de 100 utilizados; Xb <= B
# Xc: cantidad de billetes de 200 utilizados; Xc <= C
# Xd: cantidad de billetes de 500 utilizados; Xd <= D
# Xe: cantidad de billetes de 1000 utilizados; Xe <= E
# Y: salida, es la combinación de billetes a retirar.
# K: monto a retirar del cajero.

def generar_combinacion(todo_50, todo_100, todo_200, todo_500, todo_1000):
    Xa = random.randint(0, todo_50)
    Xb = random.randint(0, todo_100)
    Xc = random.randint(0, todo_200)
    Xd = random.randint(0, todo_500)
    Xe = random.randint(0, todo_1000)
    return Xa, Xb, Xc, Xd, Xe


def generar_poblacion_inicial(monto_a_retirar):
    # cantidad_poblacion_inicial = int(TOTAL_COMBINACIONES_POSIBLES * 0.001)
    todo_50 = math.ceil(monto_a_retirar / 50)
    todo_100 = math.ceil(monto_a_retirar / 100)
    todo_200 = math.ceil(monto_a_retirar / 200)
    todo_500 = math.ceil(monto_a_retirar / 500)
    todo_1000 = math.ceil(monto_a_retirar / 1000)

    # el 100 lo agregue para una poblacion mas variada
    combinaciones_posibles = todo_50 * todo_100 * todo_200 * todo_500 * todo_1000
    cantidad_poblacion_inicial = combinaciones_posibles

    if combinaciones_posibles > 1000000:
        cantidad_poblacion_inicial = 500000

    poblacion_inicial = []
    print("combinaciones posibles:", combinaciones_posibles)
    print("generando una poblacion de:", cantidad_poblacion_inicial)
    for i in range(cantidad_poblacion_inicial):
        Xa, Xb, Xc, Xd, Xe = generar_combinacion(todo_50, todo_100, todo_200, todo_500, todo_1000)
        poblacion_inicial.append({
            'billetes': (Xa, Xb, Xc, Xd, Xe)
        })
    return poblacion_inicial


# print(generar_poblacion_inicial())

def calcular_aptitud(ind, a_retirar):
    billetes = obtener_billetes(ind)
    valor = billetes[0] * 50 + billetes[1] * 100 + billetes[2] * 200 + billetes[3] * 500 + billetes[4] * 1000
    if a_retirar == valor:
        r = (a_retirar // 50) - contar_billetes(ind)
    else:
        r = abs(a_retirar - valor) * -1
    return r


def contar_billetes(ind):
    sum = 0
    for j in obtener_billetes(ind):
        sum += j
    return sum


def calcular_aptitudes(inds, a_retirar):
    resultado = []
    for i in range(0, len(inds) - 1):
        apt = calcular_aptitud(inds[i], a_retirar)
        resultado.append({
            'billetes': obtener_billetes(inds[i]),
            'aptitud': apt
        })
    return resultado


def seleccion(inds, a_retirar):
    inds = calcular_aptitudes(inds, a_retirar)
    print("poblacion antes del filtrado:", len(inds))
    individuosIterator = filter(es_apto, inds)  # removemos los que tienen aptitud -1
    inds.sort(key=obtener_aptitud, reverse=True)  # ordenamos de mejor a peor
    inds = list(individuosIterator)
    print("poblacion post filtrado:", len(inds))

    seleccionados = []
    # TODO: como sabemos cuantos tomar de los mejores?
    return inds


def mejor_individuo(individuo1, individuo2, montoARetirar):
    apt1 = calcular_aptitud(individuo1, montoARetirar)
    apt2 = calcular_aptitud(individuo2, montoARetirar)
    if apt1 > apt2:
        individuo = {
            'billetes': obtener_billetes(individuo1),
            'aptitud': apt1
        }
    else:
        individuo = {
            'billetes': obtener_billetes(individuo2),
            'aptitud': apt2
        }
    return individuo


def torneo(inds, monto_a_retirar):
    resultado = []
    for i in range(0, len(inds)):
        if i == len(inds) - 1:
            individuo = mejor_individuo(inds[i], inds[0],
                                        monto_a_retirar)  # el ultimo juega contra el primero y el anteultimo
        else:
            individuo = mejor_individuo(inds[i], inds[i + 1], monto_a_retirar)
        resultado.append(individuo)
    return resultado


# iteramos los seleccionados y hacemos cruza entre i e i+1, podriamos hacer un shuffle antes para hacer un cruzamiento mas random?
def cruzamiento(inds, monto_a_retirar):
    resultado = []

    for i in range(0, len(inds) - 1, 2):
        resultado.append(cruzar(inds[i], inds[i + 1], monto_a_retirar))
        resultado.append(cruzar(inds[i + 1], inds[i], monto_a_retirar))
    return resultado


# cruza simple. Los primeros 3 los tomamos de B, y los ultimos 2 de A.
# cruza simple. Los primeros 3 los tomamos de B, y los ultimos 2 de A.
def cruzar(indA, indB, monto_a_retirar):
    billetesA = obtener_billetes(indA)
    billetesB = obtener_billetes(indB)
    # return (obtener_billetes(indB[0]), indB[1], indB[2], indA[3], indA[4])
    return {
        'billetes': (billetesB[0], billetesB[1], billetesB[2], billetesA[3], billetesA[4])
    }


def mutar(inds):
    x = random.randint(0, len(inds) - 1)
    individuo = inds[x]
    pos = random.randint(0, len(individuo) - 1)
    billetes = list(obtener_billetes(individuo))
    billetes[pos] += 1  # ver de agregar -1 tmb
    individuo_mutado = {
        'billetes': tuple(billetes),
    }
    inds[x] = individuo_mutado
    return inds


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


def obtener_aptitud(ind):
    return ind.get('aptitud')


def obtener_billetes(individuo):
    return individuo.get('billetes')


def es_apto(individuo):
    return obtener_aptitud(individuo) >= 0


# MAIN

montoARetirar = 7350
individuos = generar_poblacion_inicial(montoARetirar)
cantidad_de_vueltas = 10000
i = 1

file = open('vuelta_mejor_aptitud.txt', 'w')

while i < cantidad_de_vueltas:
    print("ejecutando Vuelta", i)
    # seleccionados = seleccion(individuos, montoARetirar)

    print("poblacion antes del torneo", len(individuos))
    seleccionados = torneo(individuos, montoARetirar)
    seleccionados.sort(key=obtener_aptitud, reverse=True)
    file.write(str(i) + "," + str(obtener_aptitud(seleccionados[0])) + '\n')

    individuosCruzados = cruzamiento(seleccionados, montoARetirar)
    individuosMutados = mutacion(individuosCruzados)
    individuos = individuosMutados
    i += 1

print("fin de los ciclos, se ejecutaron " + str(i) + " vueltas.")


#individuos.sort(key=obtener_aptitud, reverse=True)  # ordenamos de mejor a peor
#print(individuos[0])
#a, b, c, d, e = obtener_billetes(individuos[0])
#valor = a * 50 + b * 100 + c * 200 + d * 500 + e * 1000
#print("el individuo restante cumple el valor:" + str(valor == montoARetirar))

file.close()
