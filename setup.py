import os
import urllib.request

def download_yolo_model():
    """Download YOLO model if not exists"""
    model_path = "yolov8n.pt"
    if not os.path.exists(model_path):
        print("Downloading YOLO model...")
        url = "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt"
        urllib.request.urlretrieve(url, model_path)
        print("YOLO model downloaded successfully!")

def setup_directories():
    """Create necessary directories"""
    dirs = ["profiles", "detected_faces", "models"]
    for dir_name in dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"Created directory: {dir_name}")

if __name__ == "__main__":
    setup_directories()
    download_yolo_model()
    print("\nSetup complete!")
    print("1. Install requirements: pip install -r requirements.txt")
    print("2. Add Facebook profile images to 'profiles' folder")
    print("3. Run: python main.py")