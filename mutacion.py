import random
import individuo as ind_pkg


# Se activa siempre y se ejecuta dependiendo de una probabilidad
def mutacion(inds, prb_mutacion):
    if ejecuta_mutacion(prb_mutacion):
        print("Se ejecutó mutación.")
        mutados = mutar(inds)
    else:
        mutados = inds
    return mutados


def ejecuta_mutacion(prb_mutacion):
    x = random.randint(0, 100)
    return x <= prb_mutacion


def mutar(inds):
    x = random.randint(0, len(inds) - 1)
    individuo = inds[x]
    pos = random.randint(0, len(individuo) - 1)
    billetes = list(ind_pkg.obtener_billetes(individuo))

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
