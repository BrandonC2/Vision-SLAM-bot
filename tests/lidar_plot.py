# tests/lidar_plot.py
# Live Cartesian viewer for RPLIDAR A1 (rplidar-roboticia)
# - Converts (angle°, distance mm) -> (x, y) meters
# - Filters invalid/zero/too-far points
# - Press 'S' to save a PNG to assets/screenshots/
# - Ctrl+C to quit

import os
import math
import time
import signal
import numpy as np
import matplotlib.pyplot as plt
from rplidar import RPLidar, RPLidarException

PORT = '/dev/ttyUSB0'     # change if needed (e.g., /dev/ttyUSB1)
BAUD = 115200
MAX_RANGE_M = 6.0         # show up to 6 meters around the sensor
MIN_RANGE_M = 0.10        # ignore returns closer than 10 cm (noise/reflections)
SCAN_TYPE = 'normal'      # requires rplidar-roboticia; if using 'rplidar', remove scan_type

# Output directory for screenshots
OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'screenshots')
os.makedirs(OUT_DIR, exist_ok=True)

_save_requested = False
def _on_key(event):
    global _save_requested
    if event.key in ['s', 'S']:
        _save_requested = True

def main():
    global _save_requested
    lidar = RPLidar(PORT, baudrate=BAUD, timeout=3)

    # Print info & health once
    try:
        info = lidar.get_info()
        health = lidar.get_health()
        print('INFO:', info)
        print('HEALTH:', health)
    except RPLidarException as e:
        print('Failed to read lidar info/health:', e)

    # Matplotlib setup
    plt.ion()
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.canvas.mpl_connect('key_press_event', _on_key)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-MAX_RANGE_M, MAX_RANGE_M)
    ax.set_ylim(-MAX_RANGE_M, MAX_RANGE_M)
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.5)
    ax.set_title('RPLIDAR Cartesian View (S to save, Ctrl+C to quit)')
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')

    # Origin marker (lidar location)
    origin_plot = ax.plot(0, 0, marker='o', markersize=6, label='LIDAR', linestyle='None')[0]
    scatter = ax.scatter([], [], s=4, alpha=0.85, label='points')
    ax.legend(loc='upper right')

    last_save_ts = 0.0

    def cleanup(*_):
        try:
            lidar.stop()
            lidar.stop_motor()
        except Exception:
            pass
        try:
            lidar.disconnect()
        except Exception:
            pass

    # handle Ctrl+C cleanly
    signal.signal(signal.SIGINT, lambda s, f: (_ for _ in ()).throw(KeyboardInterrupt))

    try:
        # Use scan_type if available (roboticia fork)
        iterator = lidar.iter_scans(scan_type=SCAN_TYPE)
    except TypeError:
        # Fallback for base 'rplidar' package without scan_type
        print("Note: 'scan_type' not supported; falling back to default iter_scans()")
        iterator = lidar.iter_scans()

    try:
        for i, scan in enumerate(iterator):
            # scan: list of tuples (quality, angle_deg, distance_mm)
            if not scan:
                continue

            # Convert to numpy arrays
            a_deg = np.array([m[1] for m in scan], dtype=np.float32)
            d_mm  = np.array([m[2] for m in scan], dtype=np.float32)

            # Convert to meters and filter invalids
            d_m = d_mm * 0.001
            mask = (d_m > MIN_RANGE_M) & (d_m < MAX_RANGE_M) & np.isfinite(d_m)
            a_rad = np.deg2rad(a_deg[mask])
            d_m = d_m[mask]

            # Polar -> Cartesian (lidar at origin)
            x = d_m * np.cos(a_rad)
            y = d_m * np.sin(a_rad)

            # Update plot
            scatter.set_offsets(np.c_[x, y])
            # Optionally color by distance (uncomment next 2 lines)
            # scatter.set_array(d_m)
            # scatter.set_cmap('viridis')

            # Save on demand (debounced)
            if _save_requested and (time.time() - last_save_ts) > 0.5:
                _save_requested = False
                last_save_ts = time.time()
                fname = time.strftime('lidar_cartesian_%Y%m%d_%H%M%S.png')
                path = os.path.join(OUT_DIR, fname)
                plt.savefig(path, dpi=150)
                print(f"[saved] {path}")

            plt.pause(0.001)

    except KeyboardInterrupt:
        print("\n[exit] Ctrl+C received, stopping...")
    finally:
        cleanup()
        plt.ioff()
        plt.show()

if __name__ == '__main__':
    main()
