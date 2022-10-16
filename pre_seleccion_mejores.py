import random

import main
import statistics


def pre_seleccion_de_mejores(inds, monto_a_retirar):
    inds = main.calcular_aptitudes(inds, monto_a_retirar)
    aptitudes = main.obtener_todas_las_aptitudes(inds)
    aptitud_promedio = statistics.mean(aptitudes)
    inds = calcular_aptitud_sobre_promedio(inds, aptitud_promedio)
    filtrados_mayor_a_1 = filter(aptitud_sobre_promedio_mayor_a_0, inds)
    filtrados_mayor_a_1 = list(filtrados_mayor_a_1)

    resultado = []
    for k in range(len(filtrados_mayor_a_1)):
        parte_entera = int(obtener_aptitud_sobre_promedio(filtrados_mayor_a_1[k]))
        for _ in range(parte_entera):
            resultado.append(filtrados_mayor_a_1[k])

    individuos_para_ruleta = []
    for m in range(len(inds)):
        apt_prom = obtener_aptitud_sobre_promedio(filtrados_mayor_a_1[m])
        individuos_para_ruleta.append({
            'billetes': main.obtener_billetes(filtrados_mayor_a_1[m]),
            'aptitud': apt_prom - int(apt_prom)
        })

    resultado_ruleta = ruleta(individuos_para_ruleta, len(resultado))

    resultado += resultado_ruleta
    return resultado


def ruleta(inds, cantidad_de_individuos_ya_agregados):
    aptitudes = main.obtener_todas_las_aptitudes(inds)
    aptitud_promedio = statistics.mean(aptitudes)
    inds = calcular_aptitud_sobre_promedio(inds, aptitud_promedio)
    inds.sort(key=obtener_probabilidad_acumulada, reverse=False)

    cantidad_randoms = len(
        inds) - cantidad_de_individuos_ya_agregados  # genero la cantidad de randoms necesaria para conservar el tamaño de la poblacion

    resultado = []
    for _ in range(cantidad_randoms):
        rnd = random.uniform(0, 100)
        for j in range(inds):
            if rnd <= obtener_probabilidad_acumulada(inds[j]):
                resultado.append(inds[j])
                break

    return resultado


def calcular_probabilidad_acumulada(inds):
    set_probabilidad_acumulada(inds[0], obtener_aptitud_sobre_promedio(inds[0]))

    for n in range(1, len(inds)):
        set_probabilidad_acumulada(inds[n],
                                   obtener_probabilidad_acumulada(inds[n - 1]) + obtener_aptitud_sobre_promedio(
                                       inds[n]))


def set_probabilidad_acumulada(ind, valor):
    ind.set('probabilidad_acumulada', valor)


def obtener_probabilidad_acumulada(ind):
    return ind.get('probabilidad_acumulada')


def aptitud_sobre_promedio_mayor_a_1(ind):
    return obtener_aptitud_sobre_promedio(ind) >= 1


def aptitud_sobre_promedio_menor_a_1(ind):
    return obtener_aptitud_sobre_promedio(ind) < 1


def obtener_aptitud_sobre_promedio(ind):
    return ind.get('aptitud_sobre_promedio')


def calcular_aptitud_sobre_promedio(inds, promedio):
    resultado = []
    for m in range(len(inds)):
        apt = main.obtener_aptitud(inds[m])
        resultado.append({
            'billetes': main.obtener_billetes(inds[m]),
            'aptitud': apt,
            'aptitud_sobre_promedio': apt / promedio
        })
    return resultado
