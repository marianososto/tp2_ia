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
