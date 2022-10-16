import math

import numpy as np
import random
import matplotlib.pyplot as plt
import statistics
import pre_seleccion_mejores

# import graph

# A: Cantidad de billetes de 50 disponibles
# B: Cantidad de billetes de 100 disponibles
# C: Cantidad de billetes de 200 disponibles
# D: Cantidad de billetes de 500 disponibles
# E: Cantidad de billetes de 1000 disponibles


A, B, C, D, E = 1000, 500, 250, 100, 50  # esto nos da en total $250K
TOTAL_COMBINACIONES_POSIBLES = A * B * C * D * E
PROBABILIDAD_MUTACION = 75  # 50


# Xa: cantidad de billetes de 50 utilizados; Xa <= A
# Xb: cantidad de billetes de 100 utilizados; Xb <= B
# Xc: cantidad de billetes de 200 utilizados; Xc <= C
# Xd: cantidad de billetes de 500 utilizados; Xd <= D
# Xe: cantidad de billetes de 1000 utilizados; Xe <= E
# Y: salida, es la combinación de billetes a retirar.
# K: monto a retirar del cajero.

def generar_combinacion(todo_50, todo_100, todo_200, todo_500, todo_1000):
    Xa = random.randint(0, int(todo_50 // 2) + 1)
    Xb = random.randint(0, int(todo_100 // 2) + 1)
    Xc = random.randint(0, int(todo_200 // 2) + 1)
    Xd = random.randint(0, int(todo_500 // 2) + 1)
    Xe = random.randint(0, int(todo_1000 // 2) + 1)
    return Xa, Xb, Xc, Xd, Xe


def generar_poblacion_inicial(monto_a_retirar):
    # cantidad_poblacion_inicial = int(TOTAL_COMBINACIONES_POSIBLES * 0.001)
    todo_50 = math.ceil(monto_a_retirar // 50)
    todo_100 = math.ceil(monto_a_retirar // 100)
    todo_200 = math.ceil(monto_a_retirar // 200)
    todo_500 = math.ceil(monto_a_retirar // 500)
    todo_1000 = math.ceil(monto_a_retirar // 1000)

    # el 100 lo agregue para una poblacion mas variada
    combinaciones_posibles = todo_50 * todo_100 * todo_200 * todo_500 * todo_1000
    cantidad_poblacion_inicial = combinaciones_posibles

    if combinaciones_posibles > 1000000:
        cantidad_poblacion_inicial = 5000

    poblacion_inicial = []
    print("combinaciones posibles:", combinaciones_posibles)
    print("generando una poblacion de:", cantidad_poblacion_inicial)
    for i in range(cantidad_poblacion_inicial):
        Xa, Xb, Xc, Xd, Xe = generar_combinacion(todo_50, todo_100, todo_200, todo_500, todo_1000)
        poblacion_inicial.append({
            'billetes': (Xa, Xb, Xc, Xd, Xe)
        })
    return poblacion_inicial


def calcular_aptitud(ind, a_retirar):
    billetes = obtener_billetes(ind)
    valor = billetes[0] * 50 + billetes[1] * 100 + billetes[2] * 200 + billetes[3] * 500 + billetes[4] * 1000
    if a_retirar == valor:  # return (a_retirar // 50) - contar_billetes(ind) * (1- valorNormalizado(abs(a_retirar - valor) * -1)
        r = (a_retirar // 50) - contar_billetes(ind)
    else:
        if contar_billetes(ind) > (a_retirar // 50) | (valor > 2 * a_retirar):
            r = 0
        else:
            r = ((a_retirar // 50) - contar_billetes(ind)) * (1 - ((abs(a_retirar - valor)) / a_retirar)) * 0.9
        # diferencia en valor * diferencia en billete  * ( 1 - diferencia en valor / valor a retirar)
        # r = abs(a_retirar - valor) * -1
    return r


def contar_billetes(ind):
    sum = 0
    for j in obtener_billetes(ind):
        sum += j
    return sum


def calcular_aptitudes(inds, a_retirar):
    resultado = []
    for k in range(len(inds)):
        apt = calcular_aptitud(inds[k], a_retirar)
        resultado.append({
            'billetes': obtener_billetes(inds[k]),
            'aptitud': apt
        })
    return resultado


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


def cruzar(indA, indB, monto_a_retirar):
    billetesA = obtener_billetes(indA)
    billetesB = obtener_billetes(indB)

    resultado = []
    for k in range(0, 5):
        limite = random.randint(0, 1)
        if limite == 1:
            resultado.append(billetesA[k])
        else:
            resultado.append(billetesB[k])

    return {
        'billetes': resultado
    }


def mutar(inds):
    x = random.randint(0, len(inds) - 1)
    individuo = inds[x]
    pos = random.randint(0, len(individuo) - 1)
    billetes = list(obtener_billetes(individuo))

    r = random.randint(0, 1)
    if (r == 0) & (billetes[pos] > 0):
        billetes[pos] += -1
    else:
        billetes[pos] += 1

    individuo_mutado = {
        'billetes': tuple(billetes),
    }
    inds[x] = individuo_mutado
    return inds


# se activa siempre y se ejecuta dependiendo de una probabilidad
def ejecuta_mutacion():
    x = random.randint(0, 100)
    return x <= PROBABILIDAD_MUTACION


def mutacion(inds):
    if ejecuta_mutacion():
        print("Se ejecutó mutación.")
        mutados = mutar(inds)
    else:
        mutados = inds
    return mutados


def obtener_aptitud(ind):
    return ind.get('aptitud')


def obtener_billetes(individuo):
    return individuo.get('billetes')


def es_apto(individuo):
    return obtener_aptitud(individuo) >= 0


def obtener_todas_las_aptitudes(inds):
    resultado = []
    for a in range(len(inds)):
        resultado.append(obtener_aptitud(inds[a]))
    return resultado


def billetes(inds):
    resultado = []
    for n in inds:
        resultado.append(obtener_billetes(n))
    return resultado


# MAIN
montoARetirar = 27850
individuos = generar_poblacion_inicial(montoARetirar)
cantidad_de_vueltas = 10000
i = 1

# Loggeamos vuelta por vuelta la mejor aptitud para verlo en un grafico en tiempo real.
file = open('vuelta_mejor_aptitud.txt','w')

# Loggeamos vuelta por vuelta el cromosoma con mejor aptitud.
file_cromosoma = open('cromosomas.txt', 'w')

# Logeamos el comportamiento de la poblacion vuelta por vuelta
file_log = open('ejecucion_1.log', 'w')
file_log.write('Informacion de la ejecucion\n')

while i < cantidad_de_vueltas:
    print("Ejecutando Vuelta", i, file=file_log)

    print("poblacion antes de preseleccion", len(individuos), file=file_log)
    # seleccionados = torneo(individuos, montoARetirar)
    seleccionados = pre_seleccion_mejores.pre_seleccion_de_mejores(individuos, montoARetirar)

    ordenados = seleccionados.copy()
    ordenados.sort(key=obtener_aptitud, reverse=True)

    file.write(str(i) + "," + str(obtener_aptitud(ordenados[0])) + '\n')
    file.flush()

    file_cromosoma.write(str(i) + ":" + str(obtener_billetes(ordenados[0])) + '\n')
    file_cromosoma.flush()

    billetes_inds = billetes(ordenados)
    ocurrencias_primero = billetes_inds.count(billetes_inds[0])
    print("Ocurrencias elemento mas apto: ", ocurrencias_primero, " tamaño total: ", len(ordenados), file=file_log)
    if ocurrencias_primero == len(ordenados):
        print("Toda poblacion formada por el mejor individuo. Fin.", file=file_log)
        break

    print("poblacion antes de cruzamiento", len(individuos), file=file_log)
    individuosCruzados = cruzamiento(seleccionados, montoARetirar)
    print("poblacion antes de mutacion", len(individuos), file=file_log)
    individuosMutados = mutacion(individuosCruzados)
    individuos = individuosMutados
    i += 1

print("fin de los ciclos, se ejecutaron " + str(i) + " vueltas.", file=file_log)

# cierro file descriptors.
file.close()
file_cromosoma.close()

file_log.flush()
file_log.close()
