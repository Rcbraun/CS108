import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

N = 400
NUM_COLORS = 4
COLORS = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
attraction = np.random.uniform(-1, 1, (NUM_COLORS, NUM_COLORS))

SPEED    = 0.0002
FRICTION = 0.85
FPS_MS   = 40

x = np.random.uniform(0, 1, N)
y = np.random.uniform(0, 1, N)
vx = np.zeros(N)
vy = np.zeros(N)
color_id = np.repeat(np.arange(NUM_COLORS), N // NUM_COLORS)
colors = [COLORS[c] for c in color_id]

def step():
    global x, y, vx, vy
    fx, fy = np.zeros(N), np.zeros(N)
    for i in range(NUM_COLORS):
        for j in range(NUM_COLORS):
            a = attraction[i, j]
            xi = x[color_id == i]; yi = y[color_id == i]
            xj = x[color_id == j]; yj = y[color_id == j]
            for idx, (px, py) in enumerate(zip(xi, yi)):
                dx = xj - px; dy = yj - py
                dist = np.sqrt(dx**2 + dy**2) + 1e-9
                mask = (dist < 0.2)
                f = a / dist[mask]
                global_idx = np.where(color_id == i)[0][idx]
                fx[global_idx] += np.sum(f * dx[mask] / dist[mask])
                fy[global_idx] += np.sum(f * dy[mask] / dist[mask])
    vx = (vx + fx * SPEED) * FRICTION
    vy = (vy + fy * SPEED) * FRICTION
    x = (x + vx) % 1.0
    y = (y + vy) % 1.0

fig, ax = plt.subplots(figsize=(6, 6))
sc = ax.scatter(x, y, c=colors, s=3, linewidths=0)
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
ax.set_facecolor('black'); fig.patch.set_facecolor('black')

def animate(frame):
    step()
    sc.set_offsets(np.c_[x, y])
    return [sc]

ani = FuncAnimation(fig, animate, interval=FPS_MS)
plt.tight_layout()
plt.show()