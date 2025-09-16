import csv, math
import numpy as np, matplotlib.pyplot as plt
xs, ys = [], []
with open('lidar_log.csv') as f:
    r=csv.DictReader(f)
    for row in r:
        ang=float(row['angle_deg'])*math.pi/180
        d=float(row['dist_mm'])/1000.0
        if 0.10<d<6.0:
            xs.append(d*math.cos(ang)); ys.append(d*math.sin(ang))
plt.figure(figsize=(6,6)); plt.scatter(xs, ys, s=2)
plt.gca().set_aspect('equal'); plt.xlim(-6,6); plt.ylim(-6,6)
plt.grid(True, linestyle='--', alpha=0.5)
plt.title('LIDAR Replay (Cartesian)'); plt.xlabel('X (m)'); plt.ylabel('Y (m)')
plt.show()
