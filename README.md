# VisionAI – Smart Real-Time AI Camera Application

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/) [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Build Status](https://img.shields.io/badge/Build-PyInstaller-green)](build_exe.py)

## Table of Contents
1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Architecture & Workflow](#architecture--workflow)
4. [Dependencies](#dependencies)
5. [Installation](#installation)
6. [Usage](#usage)
7. [Advanced Configuration](#advanced-configuration)
8. [Packaging & Distribution](#packaging--distribution)
9. [Project Structure](#project-structure)
10. [Contributing](#contributing)
11. [License](#license)

---
## Overview
VisionAI is a cross-platform, Python-based smart camera application providing:

- Real-time **object detection** and **tracking** powered by the ultra-light YOLOv8 Nano model
- Robust **face detection** with optional **privacy blurring**
- **Motion analysis** via background subtraction for intrusion or activity alerts
- Optional **gesture** and **pose estimation** (MediaPipe)
- **Voice control** support (SpeechRecognition & pyttsx3)
- Dual-mode GUI: **Optimized** (lightweight) and **Professional** (analytics)
- Built-in **logging**, **export**, and **packaging** utilities

Designed for rapid prototyping, security monitoring, and AI-driven camera solutions.

---
## Key Features
- **Ultra-Fast Detection**: YOLOv8-Nano inference on resized frames (640×640) every other frame for balance of speed and accuracy.
- **Object Tracking**: ID assignment, confidence history, and auto-cleanup of stale detections.
- **Face Recognition & Privacy**: Haar Cascade-based detection with a Gaussian blur option to anonymize subjects.
- **Motion Tracking**: Extracts moving contours, highlights regions of interest, and logs motion events.
- **Gesture & Pose** (Pro Mode): Hand landmarks and pose skeleton overlay via MediaPipe.
- **Voice Commands**: Start/stop camera, toggle modes, and recording via speech.
- **Recording & Screenshots**: Timestamped AVI video and JPEG captures.
- **Detection Log & Export**: In-app CSV export of detection events with timestamp, type, and details.
- **Two UI Modes**:
  - **⚡ Optimized Mode**: Single-pane interface for quick controls and live stats.
  - **🚀 Pro Mode**: Tabbed UI for settings, analytics dashboard, and log viewer.

---
## Architecture & Workflow
1. **Capture Loop**: Uses OpenCV `VideoCapture` to grab frames from camera index (default 0).
2. **Preprocessing**: Every Nth frame (configurable) is resized and passed to detection pipelines.
3. **Detection Pipelines**:
   - **Motion**: Background subtractor GPU/CPU selects ROIs.
   - **Objects**: YOLOv8 Nano returns bounding boxes; filtered by class, size, and confidence.
   - **Faces**: Haar cascades detect with position tracking.
4. **Tracking**: Simple nearest-neighbor ID assignment, confidence history, and aging-based cleanup.
5. **Rendering**: Draw boxes, labels, and overlays on live feed; update Tkinter UI.
6. **Recording & Logs**: Writes frames to video file; logs events to memory and optionally CSV.

---
## Dependencies
- `opencv-python`, `numpy`, `Pillow`
- `ultralytics`, `torch`, `torchvision` (YOLOv8)
- `mediapipe` (for gesture/pose)
- `SpeechRecognition`, `pyttsx3`, `pyaudio` (voice commands)
- `tkinter` (standard GUI)

Install all via:
```bash
pip install -r requirements.txt
```

---
## Installation
```bash
# Clone repository
git clone https://github.com/mahimapaseda/VisionAI.git
cd VisionAI

# Install Python dependencies
pip install -r requirements.txt

# Run setup (downloads YOLO model & creates folders)
python setup.py
```

---
## Usage
```bash
python vision_ai.py
```

- **Mode Selector**: Switch between Optimized and Pro in the header.
- **Start / Stop**: Begin or halt camera capture.
- **Record / Screenshot**: Toggle video recording or capture a frame.
- **Detection Toggles**: Enable/disable object, face, motion, privacy, gesture, voice.

Logs and stats update in real time. In Pro Mode, export detection log via the ⚙️ Settings tab.

---
## Advanced Configuration
Edit detection parameters in `vision_ai.py` or extract to a config:
```python
FRAME_SKIP = 2            # process every 2nd frame
YOLO_CONF = 0.4           # confidence threshold
YOLO_IOU = 0.5            # non-max suppression IoU
MOTION_AREA_THRESH = 1000 # min contour area
```
Additional advanced flags: adjust background subtractor, UI refresh rate, or log depth.

---
## Packaging & Distribution
- **Standalone EXE** (Windows):
  ```bash
  python build_exe.py
  ```
  Creates `dist/VisionAI.exe` and installer script.

- **Portable ZIP**:
  ```bash
  python create_portable.py
  ```
  Builds `VisionAI_Portable.zip` with all assets and a `Run_VisionAI.bat` launcher.

---
## Project Structure
```
VisionAI/
├── build_exe.py        # PyInstaller builder
├── cleanup.py          # Remove build artifacts & old media
├─��� create_portable.py  # Portable distribution generator
├── setup.py            # Model download & folder setup
├── vision_ai.py        # Core application and GUI
├── requirements.txt    # Python package list
├── yolov8n.pt          # Pretrained YOLOv8 Nano model
├── profiles/           # User profile images
├── recordings/         # Video output
└── screenshots/        # Captured frames
```

---
## Contributing
Contributions welcome! Fork the repo, create a feature branch, and open a pull request. Please follow the [Code of Conduct](CODE_OF_CONDUCT.md).

---
## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.