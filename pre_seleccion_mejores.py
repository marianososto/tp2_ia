import random
import statistics


def pre_seleccion_de_mejores(inds, monto_a_retirar):
    inds = calcular_aptitudes(inds, monto_a_retirar)
    aptitudes = obtener_todas_las_aptitudes(inds)
    aptitud_promedio = statistics.mean(aptitudes)
    inds = calcular_aptitud_sobre_promedio(inds, aptitud_promedio)
    filtrados_mayor_a_1 = filter(aptitud_sobre_promedio_mayor_a_1, inds)
    filtrados_mayor_a_1 = list(filtrados_mayor_a_1)

    resultado = []
    for k in range(len(filtrados_mayor_a_1) - 1):
        parte_entera = int(obtener_aptitud_sobre_promedio(filtrados_mayor_a_1[k]))
        for _ in range(parte_entera):
            resultado.append(filtrados_mayor_a_1[k])

    individuos_para_ruleta = []
    for m in range(len(filtrados_mayor_a_1) - 1):
        apt_prom = obtener_aptitud_sobre_promedio(filtrados_mayor_a_1[m])
        individuos_para_ruleta.append({
            'billetes': obtener_billetes(filtrados_mayor_a_1[m]),
            'aptitud': apt_prom - int(apt_prom)
        })

    resultado_ruleta = ruleta(individuos_para_ruleta, len(resultado))

    resultado += resultado_ruleta
    return resultado


def ruleta(inds, cantidad_de_individuos_ya_agregados):
    aptitudes = obtener_todas_las_aptitudes(inds)
    aptitud_promedio = statistics.mean(aptitudes)
    inds = calcular_aptitud_sobre_promedio(inds, aptitud_promedio)
    calcular_probabilidad_acumulada(inds)

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
    ind['probabilidad_acumulada'] = valor


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
        apt = obtener_aptitud(inds[m])
        resultado.append({
            'billetes': obtener_billetes(inds[m]),
            'aptitud': apt,
            'aptitud_sobre_promedio': apt / promedio
        })
    return resultado


##############################################################
##############################################################
##############################################################

def calcular_aptitudes(inds, a_retirar):
    resultado = []
    for k in range(0, len(inds) - 1):
        apt = calcular_aptitud(inds[k], a_retirar)
        resultado.append({
            'billetes': obtener_billetes(inds[k]),
            'aptitud': apt
        })
    return resultado


def calcular_aptitud(ind, a_retirar):
    billetes = obtener_billetes(ind)
    valor = billetes[0] * 50 + billetes[1] * 100 + billetes[2] * 200 + billetes[3] * 500 + billetes[4] * 1000
    if a_retirar == valor:  # return (a_retirar // 50) - contar_billetes(ind) * (1- valorNormalizado(abs(a_retirar - valor) * -1)
        r = (a_retirar // 50) - contar_billetes(ind)
    else:
        if contar_billetes(ind) > (a_retirar // 50) | (valor > 5 * a_retirar):
            r = 0
        else:
            r = ((a_retirar // 50) - contar_billetes(ind)) * (1 - ((abs(a_retirar - valor)) / a_retirar)) * 0.9
        # diferencia en valor * diferencia en billete  * ( 1 - diferencia en valor / valor a retirar)
        # r = abs(a_retirar - valor) * -1
    return r


def obtener_billetes(individuo):
    return individuo.get('billetes')


def contar_billetes(ind):
    sum = 0
    for j in obtener_billetes(ind):
        sum += j
    return sum


def obtener_aptitud(ind):
    return ind.get('aptitud')


def obtener_todas_las_aptitudes(inds):
    resultado = []
    for a in range(len(inds)):
        resultado.append(obtener_aptitud(inds[a]))
    return resultado
