# VisionAI – Real-Time AI Camera Detection & Analytics

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Build Status](https://img.shields.io/badge/Build-PyInstaller-green)](build_exe.py)

<p align="center">
  <em>High-performance real-time object detection, face recognition, motion tracking, and privacy protection powered by YOLOv8 and OpenCV.</em>
</p>

---

## Table of Contents
1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Quick Start](#quick-start)
4. [Installation & Setup](#installation--setup)
5. [Usage Examples](#usage-examples)
6. [Configuration](#configuration)
7. [Packaging & Distribution](#packaging--distribution)
8. [Project Structure](#project-structure)
9. [Contributing](#contributing)
10. [License](#license)

---

## Overview
VisionAI is an open-source AI camera application delivering **real-time object detection**, **face recognition**, **motion tracking**, and **privacy protection**. Utilizing the ultra-fast YOLOv8 Nano model, OpenCV, and MediaPipe, VisionAI runs on Python 3.8+ and requires minimal setup.

> **SEO Keywords:** real-time object detection, YOLOv8 Python, AI camera, face recognition, motion tracking, intelligent surveillance

---

## Key Features
- **YOLOv8-Powered Object Detection** – Accurate, low-latency detection of 80+ classes.
- **Advanced Face Recognition** – Detect faces with privacy blurring mode to protect identity.
- **Motion Tracking** – Background subtraction to highlight movement areas.
- **Gesture & Pose Estimation** – Optional MediaPipe support for hand and body pose detection.
- **Voice Control** – Speech recognition and text-to-speech commands (optional).
- **Smart Recording** – Timestamped video recording (AVI) and high-quality screenshots (JPG).
- **Detection Logging & Export** – Maintain a log of events and export to CSV.
- **Dual GUI Modes**: 
  - ⚡ **Optimized Mode** for streamlined controls and performance.  
  - 🚀 **Pro Mode** for tabbed analytics, settings, and export tools.

---

## Quick Start
```bash
# Clone the repository
git clone https://github.com/yourusername/VisionAI.git
cd VisionAI

# Install dependencies
pip install -r requirements.txt

# Initialize directories & download model
python setup.py

# Launch VisionAI
python vision_ai.py
```

---

## Installation & Setup
1. **Prerequisites**:  
   - Python 3.8 or higher  
   - Webcam or USB camera  
   - Internet connection for first-run downloads

2. **Install packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run setup script**:
   ```bash
   python setup.py
   ```
   This creates required folders (`profiles`, `detected_faces`, `models`) and downloads `yolov8n.pt`.

---

## Usage Examples
### Launch GUI
```bash
python vision_ai.py
```

- Switch between **Optimized** and **Pro** modes via the top-right selector.
- Toggle detection options: objects, faces, motion, privacy blur, gestures.
- Start/stop the camera feed, record video, and capture screenshots.

### Command-Line Cleanup Utility
```bash
python cleanup.py
```
Removes build artifacts, caches, and old media files to free storage.

---

## Configuration
Customize detection and performance parameters in `vision_ai.py` or extract to a separate config file:
```python
# YOLO settings
yolo_confidence = 0.4
yolo_iou = 0.5
max_detections = 50

# Motion detection
motion_area_threshold = 1000

# Frame processing
frame_skip = 2  # process every 2nd frame
```

---

## Packaging & Distribution
- **Standalone EXE** (Windows):
  ```bash
  python build_exe.py
  ```
  Produces `dist/VisionAI.exe` and `dist/Install_VisionAI.bat`.

- **Portable ZIP**:
  ```bash
  python create_portable.py
  ```
  Creates `VisionAI_Portable.zip` containing all necessary files.

---

## Project Structure
```bash
VisionAI/
├── build_exe.py          # PyInstaller builder script
├── cleanup.py            # Cleanup utility (artifacts, caches, media)
├── create_portable.py    # Portable ZIP builder
├── setup.py              # Directory setup & model download
├── vision_ai.py          # Main application (GUI & detection engine)
├── requirements.txt      # Python dependencies
├── yolov8n.pt            # YOLOv8 Nano model
├── profiles/             # User profile images
├── recordings/           # Saved video recordings
└── screenshots/          # Captured frames/screenshots
```

---

## Contributing
Contributions, issues, and feature requests are welcome:
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/YourFeature`
3. Commit your changes: `git commit -m "Add some feature"`
4. Push to the branch: `git push origin feature/YourFeature`
5. Open a Pull Request

Please follow the [Code of Conduct](CODE_OF_CONDUCT.md) and ensure tests pass before submitting.

---

## License
Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

*Last updated: 2024-06-30*