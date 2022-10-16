import random
import statistics
import individuo as ind_pkg
import aptitud as apt_pkg


def pre_seleccion_de_mejores(inds, monto_a_retirar):
    inds = apt_pkg.calcular_aptitudes(inds, monto_a_retirar)
    aptitudes = ind_pkg.obtener_todas_las_aptitudes(inds)
    aptitud_promedio = statistics.mean(aptitudes)
    print("Promedio: ", aptitud_promedio)
    inds = apt_pkg.calcular_aptitud_sobre_promedio(inds, aptitud_promedio)
    filtrados_mayor_a_1 = filter(aptitud_sobre_promedio_mayor_a_1, inds)
    filtrados_mayor_a_1 = list(filtrados_mayor_a_1)

    resultado = []
    for k in range(len(filtrados_mayor_a_1)):
        parte_entera = int(ind_pkg.obtener_aptitud_sobre_promedio(filtrados_mayor_a_1[k]))
        for _ in range(parte_entera):
            resultado.append(filtrados_mayor_a_1[k])

    individuos_para_ruleta = []
    for m in range(len(inds)):
        apt_prom = ind_pkg.obtener_aptitud_sobre_promedio(inds[m])
        individuos_para_ruleta.append({
            'billetes': ind_pkg.obtener_billetes(inds[m]),
            'aptitud': apt_prom - int(apt_prom)
        })

    resultado_ruleta = ruleta(individuos_para_ruleta, len(resultado))

    resultado += resultado_ruleta
    return resultado


def ruleta(inds, cantidad_de_individuos_ya_agregados):
    aptitudes = ind_pkg.obtener_todas_las_aptitudes(inds)
    aptitud_promedio = statistics.mean(aptitudes)
    print("Promedio de Ruleta: ", aptitud_promedio)
    inds = apt_pkg.calcular_aptitud_sobre_promedio(inds, aptitud_promedio)
    calcular_probabilidad_acumulada(inds)

    inds.sort(key=ind_pkg.obtener_probabilidad_acumulada, reverse=False)

    cantidad_randoms = len(inds) - cantidad_de_individuos_ya_agregados

    resultado = []
    for _ in range(cantidad_randoms):
        rnd = random.uniform(0, 100)
        for j in range(len(inds)):
            if rnd <= ind_pkg.obtener_probabilidad_acumulada(inds[j]):
                resultado.append(inds[j])
                break

    return resultado


def calcular_probabilidad_acumulada(inds):
    ind_pkg.set_probabilidad_acumulada(inds[0], ind_pkg.obtener_aptitud_sobre_promedio(inds[0]))

    for n in range(1, len(inds)):
        ind_pkg.set_probabilidad_acumulada(inds[n],
                                           ind_pkg.obtener_probabilidad_acumulada(
                                               inds[n - 1]) + ind_pkg.obtener_aptitud_sobre_promedio(
                                               inds[n]))


def aptitud_sobre_promedio_mayor_a_1(ind):
    return ind_pkg.obtener_aptitud_sobre_promedio(ind) >= 1


def aptitud_sobre_promedio_menor_a_1(ind):
    return ind_pkg.obtener_aptitud_sobre_promedio(ind) < 1
