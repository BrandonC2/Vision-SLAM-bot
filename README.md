# Vision-SLAM-bot

This project is a Raspberry Pi–based mobile robot that fuses **RPLIDAR A1**, **IMU**, **wheel encoders**, and **Pi Camera** for real-time **SLAM (Simultaneous Localization and Mapping)** and **object detection** using YOLOv8.


## To Start:
1. Clone the repo: `git clone https://github.com/BrandonC2/Vision-SLAM-bot.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Test lidar: `python tests/lidar_test.py`
4. Run YOLO camera detection: `python tests/camera_yolo.py`

## Project Status
My current progress: Lidar mapping and camera vision pipeline working.

My Next Step:
Motor + IMU integration

## Hardware I Bought
- Raspberry Pi 4
- RPLIDAR A1
- Pi Camera
- N20 encoder motors + TB6612FNG driver
- 2S LiPo + UBEC
- 9-DoF IMU (MPU-9250 class)
- Ultrasonic sensors (safety stop)

## Tools I bought that were needed (as a beginner with no experience): 
- Solder kit with the smoke absorber (to protect your health)
- 16 AWG wires 
- Wire cutter
- DEAN Y splitter
- Multimeter
- Heat shrink tube kit

## Software
- Python 3.11
- ultralytics: YOLOv8
- rplidar-roboticia
- OpenCV
- BreezySLAM

## Repo Structure
- `tests/` → standalone scripts for each sensor/module
- `nav/` → navigation & decision logic
- `slam/` → mapping integration
- `assets/` → screenshots, logs, demo videos

## Progress
- [x] Lidar scans working + visualization
- [x] Camera YOLO detection pipeline
- [ ] Motor wiring + control (coming 9/15)
- [ ] Encoder odometry
- [ ] SLAM occupancy grid
- [ ] Full integration demo

## Roadmap
- Sept 15: Motor + IMU soldering/wiring
- Sept 22: SLAM mapping demo
- Sept 30: Full integration demo video + GitHub polish

## Screenshots
* soon

## Demo Video
* soon


## What I learned

### Hardware & Power
- Safely distributed power from a LiPo battery using a UBEC for regulated 5 V output to the Raspberry Pi. 
- The importance of tying all grounds together (LiPo, UBEC, Pi, motor driver) to ensure proper signal reference.  
- Difference between logic voltage (3.3 V for Pi GPIO, IMU, motor driver control) and motor voltage (7.4 V from LiPo).

### Sensors

#### RPLIDAR
- Learned how to connect and detect lidar devices on Raspberry Pi using Linux tools:
  - `lsusb` to verify the CP210x USB–UART bridge.
  - `ls /dev/ttyUSB*` to find the serial port.
  - `dmesg` to debug when device wasn’t detected.

- Need correct baud rate 115200, or else Python library throws desync errors like Wrong body size.
- Explored two Python packages: rplidar and rplidar-roboticia which supports scan_type and is more stable.
- Converted (angle, distance) → Cartesian coordinates (x, y) and visualized with Matplotlib in both polar plots and 2D scatter plots.
- Learned to log lidar data to CSV and replay scans later without needing the hardware.

#### YOLOv8
- installed Ultralytics YOLOv8 and deployed the nano model YOLOv8n for more efficiency.
- Ran live detection from Pi Camera feed

- Learned how imgsz (input resolution) affects speed vs accuracy:
  - 320 px → faster, smoother on Pi.
  - 640 px → slower, more accurate detections.

- Adjusted confidence threshold (conf) to filter out noisy boxes.

- Added a frame rotation step with OpenCV to correct the upside-down Pi Camera feed: 
`frame = cv2.rotate(frame, cv2.ROTATE_180)`


- Wrote decision logic to turn YOLO detections into navigation commands:
  - Object in center → "STOP"
  - Object on left → "TURN RIGHT"
  - Object on right → "TURN LEFT"
  - Nothing detected → "FORWARD"

- Learned to run this pipeline with print statements first, so when motors are wired, the decisions can directly trigger motor control functions.


### Engineering Process
- It’s critical to verify voltages with a multimeter before connecting to sensitive boards.  
- The value of incremental testing: validate each subsystem individually before integration.  
- Writing “decision logic” that can run stand-alone (printing commands) before wiring motors.

### What I will learn next:
- Soldering and wiring the TB6612FNG motor driver and IMU breakout.  
- Reading encoder ticks and converting them into odometry.  
- Fusing odometry with lidar in a SLAM backend  
- Integrating ultrasonic sensors as a safety override for YOLO/lidar misses.