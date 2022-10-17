import statistics


def obtener_aptitud(individuo):
    return individuo.get('aptitud')


def obtener_billetes(individuo):
    return individuo.get('billetes')


def contar_billetes(individuo):
    sum = 0
    for j in obtener_billetes(individuo):
        sum += j
    return sum


def obtener_todas_las_aptitudes(individuos):
    resultado = []
    for a in range(len(individuos)):
        resultado.append(obtener_aptitud(individuos[a]))
    return resultado


def obtener_aptitud_sobre_promedio(ind):
    return ind.get('aptitud_sobre_promedio')


def set_probabilidad_acumulada(ind, valor):
    ind['probabilidad_acumulada'] = valor


def obtener_probabilidad_acumulada(ind):
    return ind.get('probabilidad_acumulada')


def billetes(inds):
    resultado = []
    for n in inds:
        resultado.append(obtener_billetes(n))
    return resultado
