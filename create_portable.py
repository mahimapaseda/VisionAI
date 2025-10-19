import os
import shutil
import zipfile

def create_portable_version():
    """Create portable version without PyInstaller"""
    print("📦 Creating VisionAI Portable Version...")
    
    # Create portable directory
    portable_dir = "VisionAI_Portable"
    if os.path.exists(portable_dir):
        shutil.rmtree(portable_dir)
    os.makedirs(portable_dir)
    
    # Copy essential files
    files_to_copy = [
        "vision_ai.py",
        "setup.py", 
        "requirements.txt",
        "README.md"
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, portable_dir)
            print(f"✅ Copied {file}")
    
    # Copy model if exists
    if os.path.exists("yolov8n.pt"):
        shutil.copy2("yolov8n.pt", portable_dir)
        print("✅ Copied yolov8n.pt")
    
    # Create directories
    dirs_to_create = ["profiles", "recordings", "screenshots", "detected_faces", "models"]
    for dir_name in dirs_to_create:
        os.makedirs(os.path.join(portable_dir, dir_name), exist_ok=True)
    
    # Create run script
    run_script = '''@echo off
title VisionAI - Smart Camera Detection
echo ========================================
echo    VisionAI - Smart Camera Detection
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo 📥 Please install Python 3.8+ from python.org
    echo ✅ Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Install dependencies if needed
echo 📦 Checking dependencies...
pip install -r requirements.txt --quiet

REM Download model if needed
if not exist "yolov8n.pt" (
    echo 📥 Downloading AI model...
    python setup.py
)

echo.
echo 🚀 Starting VisionAI...
echo.
python vision_ai.py

pause
'''
    
    with open(os.path.join(portable_dir, "Run_VisionAI.bat"), "w") as f:
        f.write(run_script)
    
    # Create installation guide
    install_guide = '''# VisionAI Portable - Installation Guide

## 📋 Requirements:
- Windows 10/11
- Python 3.8+ (Download from python.org)
- Webcam/Camera
- Internet connection (for first run)

## 🚀 Quick Start:
1. **Install Python** (if not installed):
   - Go to python.org
   - Download Python 3.8+
   - ✅ CHECK "Add Python to PATH" during installation

2. **Run VisionAI**:
   - Double-click "Run_VisionAI.bat"
   - First run will install dependencies automatically
   - Choose mode: ⚡ Optimized or 🚀 Pro

## 📁 Folder Structure:
- `vision_ai.py` - Main application
- `Run_VisionAI.bat` - Easy launcher
- `requirements.txt` - Dependencies list
- `profiles/` - Profile images
- `recordings/` - Video recordings
- `screenshots/` - Screenshots

## 🔧 Manual Installation:
If automatic installation fails:
```
pip install opencv-python numpy Pillow ultralytics torch torchvision
python setup.py
python vision_ai.py
```

## 📞 Support:
- Make sure camera permissions are enabled
- Run as Administrator if needed
- Check antivirus settings if blocked

Enjoy VisionAI! 🎯
'''
    
    with open(os.path.join(portable_dir, "INSTALL_GUIDE.md"), "w") as f:
        f.write(install_guide)
    
    # Create ZIP file
    zip_filename = "VisionAI_Portable.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(portable_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, portable_dir)
                zipf.write(file_path, arc_path)
    
    print(f"\n✅ Portable version created!")
    print(f"📁 Folder: {portable_dir}/")
    print(f"📦 ZIP file: {zip_filename}")
    print(f"📋 Size: ~{os.path.getsize(zip_filename) / 1024:.1f} KB")
    
    print("\n🚀 Distribution ready!")
    print("📤 Share the ZIP file or folder")
    print("📋 Users just need to run 'Run_VisionAI.bat'")

if __name__ == "__main__":
    create_portable_version()