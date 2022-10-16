def obtener_aptitud(individuo):
    return individuo.get('aptitud')


def obtener_billetes(individuo):
    return individuo.get('billetes')


def contar_billetes(individuo):
    sum = 0
    for j in obtener_billetes(individuo):
        sum += j
    return sum
