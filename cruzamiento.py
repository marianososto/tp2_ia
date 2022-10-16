import individuo as ind_pkg
import random


def cruzamiento(inds, monto_a_retirar):
    resultado = []

    for i in range(0, len(inds) - 1, 2):
        resultado.append(cruzar(inds[i], inds[i + 1], monto_a_retirar))
        resultado.append(cruzar(inds[i + 1], inds[i], monto_a_retirar))
    return resultado


def cruzar(indA, indB, monto_a_retirar):
    billetesA = ind_pkg.obtener_billetes(indA)
    billetesB = ind_pkg.obtener_billetes(indB)

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
