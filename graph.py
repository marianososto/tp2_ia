"""
Levantar este codigo en un terminal utlizando python. Por ejemplo:
python3.8 graph.py

Esto creara una ventana con un grafico para ver en tiempo real el comportamiento de la mejor aptitud a lo largo de las vueltas.
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)


xs = []
ys = []


def animate(i):

    graph_data = open('vuelta_mejor_aptitud.txt', 'r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(float(x))
            ys.append(float(y))
    ax1.clear()
    plt.title('Evolucion de la Aptitud')
    plt.xlabel("Vuelta")
    plt.ylabel("Mejor Aptitud")
    ax1.plot(xs, ys)


ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()