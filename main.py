import pre_seleccion_mejores
import cruzamiento as cruz_pkg
import mutacion as mut_pkg
import individuo as ind_pkg
import poblacion_inicial as pob_inic_pkg

# import graph

# A: Cantidad de billetes de 50 disponibles
# B: Cantidad de billetes de 100 disponibles
# C: Cantidad de billetes de 200 disponibles
# D: Cantidad de billetes de 500 disponibles
# E: Cantidad de billetes de 1000 disponibles


A, B, C, D, E = 1000, 500, 250, 100, 50  # esto nos da en total $250K
TOTAL_COMBINACIONES_POSIBLES = A * B * C * D * E
PROBABILIDAD_MUTACION = 25  # 50

# MAIN
montoARetirar = 27850
individuos = pob_inic_pkg.generar_poblacion_inicial(montoARetirar)
cantidad_de_vueltas = 10000
i = 1

# Loggeamos vuelta por vuelta la mejor aptitud para verlo en un grafico en tiempo real.
file = open('vuelta_mejor_aptitud.txt', 'w')

# Loggeamos vuelta por vuelta el cromosoma con mejor aptitud.
file_cromosoma = open('cromosomas.txt', 'w')

# Logeamos el comportamiento de la poblacion vuelta por vuelta
file_log = open('log_ejecucion.csv', 'w')
file_log.write('Informacion de la ejecucion\n')

while i < cantidad_de_vueltas:
    print("Ejecutando Vuelta", i, file=file_log)

    print("Poblacion antes de seleccion", len(individuos), file=file_log)
    # seleccionados = torneo(individuos, montoARetirar)
    seleccionados = pre_seleccion_mejores.pre_seleccion_de_mejores(individuos, montoARetirar)

    ordenados = seleccionados.copy()
    ordenados.sort(key=ind_pkg.obtener_aptitud, reverse=True)

    file.write(str(i) + "," + str(ind_pkg.obtener_aptitud(ordenados[0])) + '\n')
    file.flush()

    file_cromosoma.write(str(i) + ":" + str(ind_pkg.obtener_billetes(ordenados[0])) + '\n')
    file_cromosoma.flush()

    billetes_inds = ind_pkg.billetes(ordenados)
    ocurrencias_primero = billetes_inds.count(billetes_inds[0])
    print("Ocurrencias elemento mas apto: ", ocurrencias_primero, " tamaño total: ", len(ordenados), file=file_log)
    if ocurrencias_primero == len(ordenados):
        print("Toda poblacion formada por el mejor individuo. Fin.", file=file_log)
        break

    print("Poblacion antes de cruzamiento", len(individuos), file=file_log)
    individuosCruzados = cruz_pkg.cruzamiento(seleccionados, montoARetirar)
    print("Poblacion antes de mutacion", len(individuos), file=file_log)
    individuosMutados = mut_pkg.mutacion(individuosCruzados, PROBABILIDAD_MUTACION)
    individuos = individuosMutados
    i += 1

print("fin de los ciclos, se ejecutaron " + str(i) + " vueltas.", file=file_log)

# cierro file descriptors.
file.close()
file_cromosoma.close()

file_log.flush()
file_log.close()
