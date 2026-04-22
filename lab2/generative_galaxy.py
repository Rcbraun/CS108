import numpy as np
import matplotlib.pyplot as plt

np.random.seed(None)

NUM_ARMS = 2
STARS_PER_ARM = 2000
NOISE = 0.18
SPREAD = 0.12

fig, ax = plt.subplots(figsize=(8, 8), facecolor='black')
ax.set_facecolor('black')
ax.axis('off')

cmap = plt.cm.Blues

for arm in range(NUM_ARMS):
    offset = (2 * np.pi / NUM_ARMS) * arm
    theta = np.linspace(0.3, 4.5 * np.pi, STARS_PER_ARM)
    r = 0.12 * np.exp(0.25 * theta)
    r += np.random.normal(0, SPREAD * r, STARS_PER_ARM)
    x = r * np.cos(theta + offset) + np.random.normal(0, NOISE * 0.1, STARS_PER_ARM)
    y = r * np.sin(theta + offset) + np.random.normal(0, NOISE * 0.1, STARS_PER_ARM)
    dist = np.sqrt(x**2 + y**2)
    brightness = np.clip(1 - dist / dist.max(), 0.1, 1)
    colors = cmap(brightness * 0.9 + 0.1)
    ax.scatter(x, y, c=colors, s=0.4, linewidths=0, alpha=0.6)

# Core glow
for radius, alpha in [(0.05, 0.3), (0.12, 0.15), (0.25, 0.08)]:
    core = plt.Circle((0, 0), radius, color='white', alpha=alpha)
    ax.add_patch(core)

# Background stars
bx = np.random.uniform(-2, 2, 1500)
by = np.random.uniform(-2, 2, 1500)
ax.scatter(bx, by, c='white', s=0.2, alpha=0.3)

ax.set_xlim(-2, 2); ax.set_ylim(-2, 2)
plt.tight_layout()
plt.savefig('galaxy.png', dpi=150, bbox_inches='tight', facecolor='black')
plt.show()