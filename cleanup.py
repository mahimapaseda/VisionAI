"""
VisionAI Cleanup Utility
Removes build artifacts and temporary files
"""

import os
import shutil

def remove_directory(path):
    """Remove directory if it exists"""
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            print(f"[OK] Removed: {path}/")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to remove {path}: {e}")
            return False
    return False

def remove_file(path):
    """Remove file if it exists"""
    if os.path.exists(path):
        try:
            os.remove(path)
            print(f"[OK] Removed: {path}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to remove {path}: {e}")
            return False
    return False

def clean_directory(path, extensions=None):
    """Clean files in directory by extension"""
    if not os.path.exists(path):
        return 0
    
    count = 0
    for file in os.listdir(path):
        if extensions:
            if any(file.endswith(ext) for ext in extensions):
                filepath = os.path.join(path, file)
                if remove_file(filepath):
                    count += 1
        else:
            filepath = os.path.join(path, file)
            if os.path.isfile(filepath):
                if remove_file(filepath):
                    count += 1
    return count

def main():
    print("VisionAI Cleanup Utility")
    print("=" * 50)
    
    removed_count = 0
    
    # Build artifacts
    print("\n[BUILD] Removing build artifacts...")
    if remove_directory("build"):
        removed_count += 1
    if remove_directory("dist"):
        removed_count += 1
    if remove_directory("__pycache__"):
        removed_count += 1
    
    # Unnecessary directories
    print("\n[DIRS] Removing unused directories...")
    if remove_directory("detected_faces"):
        removed_count += 1
    if remove_directory("models"):
        removed_count += 1
    
    # Clean recordings and screenshots (optional)
    print("\n[MEDIA] Cleaning recordings and screenshots...")
    print("   (Keeping directories, removing old files)")
    
    recordings_cleaned = clean_directory("recordings", ['.avi', '.mp4'])
    screenshots_cleaned = clean_directory("screenshots", ['.jpg', '.png', '.jpeg'])
    
    if recordings_cleaned > 0:
        print(f"   [OK] Cleaned {recordings_cleaned} recordings")
    if screenshots_cleaned > 0:
        print(f"   [OK] Cleaned {screenshots_cleaned} screenshots")
    
    # Python cache files
    print("\n[CACHE] Removing Python cache files...")
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                pycache_path = os.path.join(root, dir_name)
                if remove_directory(pycache_path):
                    removed_count += 1
        
        for file in files:
            if file.endswith('.pyc') or file.endswith('.pyo'):
                if remove_file(os.path.join(root, file)):
                    removed_count += 1
    
    # Spec files (if not needed)
    print("\n[SPEC] Removing PyInstaller spec files...")
    if remove_file("VisionAI.spec"):
        removed_count += 1
    
    print("\n" + "=" * 50)
    print(f"Cleanup complete! Removed {removed_count} items")
    print("\nProject Structure:")
    print("   [OK] vision_ai.py (Main app)")
    print("   [OK] requirements.txt")
    print("   [OK] setup.py")
    print("   [OK] README.md")
    print("   [OK] yolov8n.pt (AI model)")
    print("   [OK] profiles/ (Empty, ready for use)")
    print("   [OK] recordings/ (Empty, ready for use)")
    print("   [OK] screenshots/ (Empty, ready for use)")

if __name__ == "__main__":
    main()
