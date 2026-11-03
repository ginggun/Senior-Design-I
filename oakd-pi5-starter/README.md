# Senior Design — OAK-D Lite + Raspberry Pi 5 Starter

**Status:** preliminary, not hardware-tested. This code is for controlled bench demonstrations only and **not** a mobility safety device. Do not use it for unsupervised navigation.

## Goal

Start with a basic three-region depth warning prototype that can run without a camera. When hardware arrives, try DepthAI v3 stereo-depth streaming on Raspberry Pi 5. YOLO / spatial object detection and GPS / LiDAR integration are **future tasks**, not implemented here.

## Project structure

```text
oakd-pi5-starter/
├── README.md
├── .gitignore
├── requirements-hardware.txt
├── simulate.py                 # NO HARDWARE REQUIRED
├── camera_depth.py             # OAK-D Lite depth, experimental
├── src/
│   └── obstacle_logic.py      # reusable warning logic
└── tests/
    └── test_obstacle_logic.py
```

## Try now — Windows / VS Code / Mac / Linux

Requires Python **3.10+**. From the `oakd-pi5-starter` directory:

```bash
python simulate.py
python -m unittest discover -s tests -v
```

On some machines the command may be `python3` or Windows `py -3` instead of `python`.

The example prints a center-region hazard at around 0.9m. The example is simulated, not real camera output.

## When the Pi 5 + OAK-D Lite arrives

1. Power Raspberry Pi 5 with an appropriate supply (official 27W USB-C recommended for bench setup). Connect OAK-D Lite to USB 3.0 with a suitable data cable. Consider a powered USB hub if supply/current issues arise.
2. Install Raspberry Pi OS 64-bit; open a terminal on the Pi.
3. Create and activate a virtual environment:

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip
cd ~/Senior-Design-I/oakd-pi5-starter  # adjust to your actual folder
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-hardware.txt
```

4. Before using our experimental script, follow the **official Luxonis Stereo Depth example** below and verify the camera streams. On a headless Pi, GUI examples need a desktop session or modification.
5. Try `python camera_depth.py` as an **experimental** depth-stream integration. API behavior has not been validated against your exact Pi OS, DepthAI package, and camera firmware. Fix discrepancies against the official docs.
6. Check camera visibility/USB, valid depths, FPS, processing load, power stability and physical depth distances (0.5, 1, 2, 3 m).

## Next development phases (not yet implemented)

- YOLOv6-Nano on the OAK's RVC2 (no model training required for the demo).
- Spatial Detection: combine object class / box with stereo depth to calculate approximate distance.
- Data contract to teammates: `timestamp`, `sensor`, `region`, `distance_m`, `validity`, `source`.
- Audible / haptic alerts; design fail-safe behavior for invalid or missing depth.
- Motion, sunlight, narrow-post and curb test plan; evaluate false negatives.

## How to interpret the depth-only prototype

The warning logic crops the image vertically, partitions it into **left / center / right**, ignores invalid values and uses a near-distance percentile of valid pixels. This is a **toy algorithm**, not a physically calibrated path-clearance detector. It can falsely warn on the floor or miss small objects; never infer that a route is safe from its output. Calibration, floor filtering, camera pose, synchronization, latency testing, and temporal smoothing are needed later.

## Official Luxonis documentation (DepthAI v3)

- [Stereo Depth Example](https://docs.luxonis.com/software-v3/depthai/examples/stereo_depth/stereo_depth)
- [StereoDepth Node](https://docs.luxonis.com/software-v3/depthai/depthai-components/nodes/stereo_depth)
- [YOLO Detection Example](https://docs.luxonis.com/software-v3/depthai/examples/detection_network/detection_network)
- [Spatial Detection Example](https://docs.luxonis.com/software-v3/depthai/examples/spatial_detection_network/spatial_detection)
- [DepthAI Installation](https://docs.luxonis.com/software-v3/depthai)

## GitHub workflow

Copy this folder into your existing Senior Design repo, then from the repo root:

```bash
git add oakd-pi5-starter/
git commit -m "Add OAK-D Lite and Pi 5 camera starter"
git push origin main
```

You should first check `git status` and confirm the folder location and current branch. Never commit private keys, access tokens, credentials, recorded personal video, large model files, or the `.venv` directory.
