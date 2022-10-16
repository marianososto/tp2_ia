import random
import math


def generar_combinacion(todo_50, todo_100, todo_200, todo_500, todo_1000):
    Xa = random.randint(0, int(todo_50 // 2) + 1)
    Xb = random.randint(0, int(todo_100 // 2) + 1)
    Xc = random.randint(0, int(todo_200 // 2) + 1)
    Xd = random.randint(0, int(todo_500 // 2) + 1)
    Xe = random.randint(0, int(todo_1000 // 2) + 1)
    return Xa, Xb, Xc, Xd, Xe


def generar_poblacion_inicial(monto_a_retirar):
    todo_50 = math.ceil(monto_a_retirar // 50)
    todo_100 = math.ceil(monto_a_retirar // 100)
    todo_200 = math.ceil(monto_a_retirar // 200)
    todo_500 = math.ceil(monto_a_retirar // 500)
    todo_1000 = math.ceil(monto_a_retirar // 1000)

    # el 100 lo agregue para una poblacion mas variada
    combinaciones_posibles = todo_50 * todo_100 * todo_200 * todo_500 * todo_1000

    cantidad_poblacion_inicial = 5000

    poblacion_inicial = []
    print("combinaciones posibles:", combinaciones_posibles)
    print("generando una poblacion de:", cantidad_poblacion_inicial)
    for i in range(cantidad_poblacion_inicial):
        xa, xb, xc, xd, xe = generar_combinacion(todo_50, todo_100, todo_200, todo_500, todo_1000)
        poblacion_inicial.append({
            'billetes': (xa, xb, xc, xd, xe)
        })
    return poblacion_inicial
