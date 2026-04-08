import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Grid size
N = 200

# Parameters (these control the pattern!)
Du, Dv = 0.16, 0.08
F, k = 0.060, 0.062

# Initialize chemicals
U = np.ones((N, N))
V = np.zeros((N, N))

# Seed in the center
r = 20
U[N//2 - r:N//2 + r, N//2 - r:N//2 + r] = 0.50
V[N//2 - r:N//2 + r, N//2 - r:N//2 + r] = 0.25

def laplacian(Z):
    return (
        -4 * Z
        + np.roll(Z, (1, 0), (0, 1))
        + np.roll(Z, (-1, 0), (0, 1))
        + np.roll(Z, (0, 1), (0, 1))
        + np.roll(Z, (0, -1), (0, 1))
    )

def update(frame):
    global U, V

    Lu = laplacian(U)
    Lv = laplacian(V)

    reaction = U * V * V

    U += (Du * Lu - reaction + F * (1 - U))
    V += (Dv * Lv + reaction - (F + k) * V)

    im.set_array(V)
    return [im]

fig, ax = plt.subplots()
im = ax.imshow(V, cmap='inferno', interpolation='bilinear')
ax.axis('off')

# --- Mouse interaction ---
brush = 5
def on_move(event):
    if event.inaxes and event.button == 1:
        x, y = int(event.xdata), int(event.ydata)
        V[y-brush:y+brush, x-brush:x+brush] = 0.5
        U[y-brush:y+brush, x-brush:x+brush] = 0.25

fig.canvas.mpl_connect('motion_notify_event', on_move)

ani = FuncAnimation(fig, update, frames=10000, interval=1)

plt.tight_layout()
plt.show()