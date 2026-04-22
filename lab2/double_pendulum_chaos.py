import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

g, L1, L2, m1, m2 = 9.8, 1.0, 1.0, 1.0, 1.0
dt = 0.02
N = 30  # number of pendulums

# Nearly identical starting angles
base_angle = np.pi * 0.2
theta1 = np.full(N, base_angle) + np.linspace(-0.001, 0.001, N)
theta2 = np.full(N, base_angle) + np.linspace(-0.001, 0.001, N)
dth1 = np.zeros(N)
dth2 = np.zeros(N)

trail_x2 = [[] for _ in range(N)]
trail_y2 = [[] for _ in range(N)]
TRAIL_LEN = 120
cmap = plt.cm.plasma

def derivs(t1, t2, dt1, dt2):
    d = t1 - t2
    denom1 = (m1 + m2) * L1 - m2 * L1 * np.cos(d)**2
    denom2 = (L2 / L1) * denom1
    a1 = (m2*L1*dt1**2*np.sin(d)*np.cos(d)
          + m2*g*np.sin(t2)*np.cos(d)
          + m2*L2*dt2**2*np.sin(d)
          - (m1+m2)*g*np.sin(t1)) / denom1
    a2 = (-m2*L2*dt2**2*np.sin(d)*np.cos(d)
          + (m1+m2)*(g*np.sin(t1)*np.cos(d)
          - L1*dt1**2*np.sin(d)
          - g*np.sin(t2))) / denom2
    return a1, a2

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-2.5, 2.5); ax.set_ylim(-2.5, 2.5)
ax.set_facecolor('black'); fig.patch.set_facecolor('black')
ax.axis('off')
lines = [ax.plot([], [], lw=0.8, alpha=0.7,
         color=cmap(i/N))[0] for i in range(N)]

def animate(frame):
    global theta1, theta2, dth1, dth2
    for _ in range(3):
        a1, a2 = derivs(theta1, theta2, dth1, dth2)
        dth1 += a1 * dt; dth2 += a2 * dt
        theta1 += dth1 * dt; theta2 += dth2 * dt
    x1 =  L1 * np.sin(theta1)
    y1 = -L1 * np.cos(theta1)
    x2 = x1 + L2 * np.sin(theta2)
    y2 = y1 - L2 * np.cos(theta2)
    for i in range(N):
        trail_x2[i].append(x2[i])
        trail_y2[i].append(y2[i])
        if len(trail_x2[i]) > TRAIL_LEN:
            trail_x2[i].pop(0); trail_y2[i].pop(0)
        lines[i].set_data(trail_x2[i], trail_y2[i])
    return lines

ani = FuncAnimation(fig, animate, interval=16)
plt.tight_layout()
plt.show()