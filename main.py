import math

import numpy as np
import random
import matplotlib.pyplot as plt

# A: Cantidad de billetes de 50 disponibles
# B: Cantidad de billetes de 100 disponibles
# C: Cantidad de billetes de 200 disponibles
# D: Cantidad de billetes de 500 disponibles
# E: Cantidad de billetes de 1000 disponibles


A, B, C, D, E = 1000, 500, 250, 100, 50  # esto nos da en total $250K
TOTAL_COMBINACIONES_POSIBLES = A * B * C * D * E


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

    if combinaciones_posibles > 1000000:
        cantidad_poblacion_inicial = 100000
    else:
        cantidad_poblacion_inicial = 10000

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


# iteramos los seleccionados y hacemos cruza entre i e i+1, podriamos hacer un shuffle antes para hacer un cruzamiento mas random?
def cruzamiento(inds):
    probabilidad_de_cruzamiento = random.randint(1, 100)

    if probabilidad_de_cruzamiento > 70:
        resultado = []
        for k in range(0, len(inds) - 2):
            resultado.append(cruzar(inds[k], inds[k + 1]))
        return resultado
    else:
        return inds


# cruza simple. Los primeros 3 los tomamos de B, y los ultimos 2 de A.
def cruzar(ind_a, ind_b):
    billetes_a = obtener_billetes(ind_a)
    billetes_b = obtener_billetes(ind_b)
    return {
        'billetes': (billetes_b[0], billetes_b[1], billetes_b[2], billetes_a[3], billetes_a[4]),
        'aptitud': 0
    }


def mutar(individuo):
    probabilidad_de_mutacion = random.randint(1, 100)
    if probabilidad_de_mutacion > 90:
        a, b, c, d, e = obtener_billetes(individuo)
        return {
            'billetes': (a, b, c, d, e),
            'aptitud': obtener_aptitud(individuo)
        }
    return individuo


def mutacion(inds):
    mutados = []
    for i in range(len(inds)):
        mutados.append(mutar(inds[i]))
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
i = 0

while i < cantidad_de_vueltas:
    print("ejecutando Vuelta", i)
    seleccionados = seleccion(individuos, montoARetirar)
    if len(seleccionados) <= 1: # condicion de corte
        print("se filtró toda la poblacion, finalizando ejecucion.")
        break

    individuosCruzados = cruzamiento(seleccionados)
    individuosMutados = mutacion(individuosCruzados)
    individuos = individuosMutados
    i += 1

print("sali del while")
individuos.sort(key=obtener_aptitud, reverse=True)  # ordenamos de mejor a peor
print(individuos[0])
