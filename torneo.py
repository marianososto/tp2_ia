import individuo as ind_pkg
import aptitud as apt_pkg


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


def mejor_individuo(individuo1, individuo2, montoARetirar):
    apt1 = apt_pkg.calcular_aptitud(individuo1, montoARetirar)
    apt2 = apt_pkg.calcular_aptitud(individuo2, montoARetirar)
    if apt1 > apt2:
        individuo = {
            'billetes': ind_pkg.obtener_billetes(individuo1),
            'aptitud': apt1
        }
    else:
        individuo = {
            'billetes': ind_pkg.obtener_billetes(individuo2),
            'aptitud': apt2
        }
    return individuo
