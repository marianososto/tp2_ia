import individuo


def calcular_aptitud(ind, a_retirar):
    billetes = individuo.obtener_billetes(ind)
    valor = billetes[0] * 50 + billetes[1] * 100 + billetes[2] * 200 + billetes[3] * 500 + billetes[4] * 1000
    if a_retirar == valor:  # return (a_retirar // 50) - contar_billetes(ind) * (1- valorNormalizado(abs(a_retirar - valor) * -1)
        r = (a_retirar // 50) - individuo.contar_billetes(ind)
    else:
        if individuo.contar_billetes(ind) > (a_retirar // 50) | (valor > 2 * a_retirar):
            r = 0
        else:
            r = ((a_retirar // 50) - individuo.contar_billetes(ind)) * (
                    1 - ((abs(a_retirar - valor)) / a_retirar)) * 0.9
        # diferencia en valor * diferencia en billete  * ( 1 - diferencia en valor / valor a retirar)
        # r = abs(a_retirar - valor) * -1
    return r


def es_apto(individuo):
    return individuo.obtener_aptitud(individuo) >= 0


def calcular_aptitudes(inds, a_retirar):
    resultado = []
    for k in range(len(inds)):
        apt = calcular_aptitud(inds[k], a_retirar)
        resultado.append({
            'billetes': individuo.obtener_billetes(inds[k]),
            'aptitud': apt
        })
    return resultado


def obtener_todas_las_aptitudes(inds):
    resultado = []
    for a in range(len(inds)):
        resultado.append(individuo.obtener_aptitud(inds[a]))
    return resultado


def calcular_aptitud_sobre_promedio(inds, promedio):
    resultado = []
    for m in range(len(inds)):
        apt = individuo.obtener_aptitud(inds[m])
        resultado.append({
            'billetes': individuo.obtener_billetes(inds[m]),
            'aptitud': apt,
            'aptitud_sobre_promedio': apt / promedio
        })
    return resultado
