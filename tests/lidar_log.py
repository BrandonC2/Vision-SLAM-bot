import csv, time
from rplidar import RPLidar
PORT='/dev/ttyUSB0'; BAUD=115200
with RPLidar(PORT, baudrate=BAUD) as lidar:
    t0=time.time()
    with open('lidar_log.csv','w',newline='') as f:
        w=csv.writer(f); w.writerow(['t','angle_deg','dist_mm'])
        for scan in lidar.iter_scans(scan_type='normal'):
            t=time.time()-t0
            for _,ang,dist in scan:
                w.writerow([f'{t:.3f}', f'{ang:.2f}', int(dist)])
            if t>15: break
