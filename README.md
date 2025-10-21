# VisionAI

## 🌟 Overview

![VisionAI Demo](./video.gif)

**VisionAI** is a cross-platform, Python-based smart camera application that delivers real-time AI-powered features in a responsive GUI. Built with YOLOv8, OpenCV, and MediaPipe, it offers seamless object detection, face recognition with privacy blurring, motion tracking, gesture support, and voice commands.

Experience live AI detection: **[GitHub Repo](https://github.com/mahimapaseda/VisionAI)**

---

### 🎯 Key Features

- **🔍 Ultra-Fast Object Detection** – YOLOv8 Nano inference at 640×640 resolution
- **👁️ Face Recognition & Privacy Blurring** – Haar Cascade detection with optional blur for anonymity
- **🏃 Motion Tracking & Alerts** – Background subtraction highlights moving objects in real time
- **🤚 Gesture & Pose Estimation** (Pro Mode) – Hand and body tracking via MediaPipe
- **🎤 Voice Commands** – Control start/stop, recording, and detection toggles with speech
- **🖼️ Recording & Screenshots** – Timestamped AVI videos and JPEG snapshots
- **📊 Event Logging & CSV Export** – Automated detection logs for analysis
- **⚡ Dual GUI Modes** – Optimized Mode for lightweight use, Pro Mode for advanced analytics
- **📦 Easy Distribution** – Create standalone EXE or portable ZIP package

---

### 🎥 Video Demo

> **📹 [Watch Full Demo](./video.gif)** – Explore VisionAI features: live object detection, face blurring, motion alerts, and the Pro analytics dashboard.

**Demo Highlights:**

- 🔍 Real-time detection of multiple object classes
- 👁️ Privacy blurring of faces on demand
- 🏃 Highlighted motion regions with area-based alerts
- 🤚 Gesture controls and pose skeleton overlay
- 📊 Exportable CSV log from the analytics panel

---

## 🛠️ Installation
```bash
# Clone repository
git clone https://github.com/mahimapaseda/VisionAI.git
cd VisionAI

# Install dependencies
pip install -r requirements.txt

# Setup (downloads YOLO model & creates folders)
python setup.py

# Launch application
python vision_ai.py
```

---

## ⚖️ License
Distributed under the MIT License. See [LICENSE](LICENSE) for details.
