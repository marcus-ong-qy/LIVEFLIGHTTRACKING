import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation

fig, ax = plt.subplots()

x = np.arange(0, 2 * np.pi, 0.01)
f = lambda x: np.sin(x)
line, = ax.plot(x, f(x))

scat = plt.scatter([], [], s=20, alpha=1, color="purple", edgecolors='none')
ann_list = []


def animate(j):
    for i, a in enumerate(ann_list):
        a.remove()
    ann_list[:] = []

    n = np.random.rand(5) * 6
    scat.set_offsets([(r, f(r)) for r in n])
    for j in range(len(n)):
        ann = plt.annotate("{:.2f}".format(n[j]), xy=(n[j], f(n[j])), color="purple", fontsize=12)
        ann_list.append(ann)


ani = matplotlib.animation.FuncAnimation(fig, animate, frames=20, interval=360)
ani.save(__file__ + ".gif", fps=3)
plt.show()
