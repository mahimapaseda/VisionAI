# VisionAI

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Build](https://img.shields.io/badge/Build-PyInstaller-green)](build_exe.py)

**Smart Real-Time AI Camera** application with object detection, face recognition, motion tracking, and privacy protection.

---

## 🔍 Features
- **Ultra-Fast Object Detection** (YOLOv8 Nano)
- **Face Detection & Privacy Blurring**
- **Motion Analysis & Alerts** (background subtraction)
- **Gesture & Pose Recognition** (optional via MediaPipe)
- **Voice Commands** (optional speech recognition & TTS)
- **Dual GUI Modes** Optimized & Professional
- **Recording & Screenshots** (timestamped video/snapshots)
- **Event Logging & CSV Export**
- **Standalone EXE** (PyInstaller) & **Portable ZIP** distribution

---

## 🛠️ Installation
```bash
# 1. Clone the repo
git clone https://github.com/mahimapaseda/VisionAI.git
cd VisionAI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup (downloads model + creates folders)
python setup.py
```

---

## 🚀 Usage
```bash
python vision_ai.py
```

1. **Select Mode**: Toggle Optimized vs. Professional in header
2. **Toggle Detections**: Objects, Faces, Motion, Privacy, Gestures, Voice
3. **Controls**: Start/Stop camera, Record video, Capture screenshot
4. **Export** (Pro Mode): Download CSV log of detection events

---

## ⚙️ Configuration
Edit `vision_ai.py` constants or define a separate config file:
```python
FRAME_SKIP = 2       # Process every 2nd frame
YOLO_CONF = 0.4      # YOLO confidence threshold
YOLO_IOU = 0.5       # Non-max suppression IoU
MOTION_AREA = 1000   # Min contour area for motion
```

---

## 📦 Distribution
- **Standalone EXE**:
  ```bash
  python build_exe.py
  ```
- **Portable ZIP**:
  ```bash
  python create_portable.py
  ```

---

## 📂 Project Structure
```
VisionAI/
├── build_exe.py         # Create Windows executable
├── cleanup.py           # Remove build artifacts & old media
├── create_portable.py   # Portable ZIP generator
├── setup.py             # Download model & create dirs
├── vision_ai.py         # Main application
├── requirements.txt     # Python dependencies
├── yolov8n.pt           # Pretrained model
├── profiles/            # User face images
├── recordings/          # Video outputs
└── screenshots/         # Captured frames
```

---

## 👨‍💻 Author
**Mahima Paseda**  
GitHub: [@mahimapaseda](https://github.com/mahimapaseda)

**📞 Support**  
Email: mahimapaseda@example.com  
Issues: [Create a new GitHub issue](https://github.com/mahimapaseda/VisionAI/issues)

---

## ⚖️ License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.