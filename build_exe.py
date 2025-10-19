import os
import subprocess
import sys

def install_pyinstaller():
    """Install PyInstaller if not available"""
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installed successfully")

def create_exe():
    """Create executable file"""
    print("🔨 Building VisionAI executable...")
    
    # Use python -m PyInstaller to avoid PATH issues
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--noconsole",
        "--name=VisionAI",
        "--distpath=dist",
        "--workpath=build",
        "--specpath=."
    ]
    
    # Add data files if they exist
    if os.path.exists("yolov8n.pt"):
        cmd.extend(["--add-data", "yolov8n.pt;."])
    
    cmd.append("vision_ai.py")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Executable created successfully!")
            print("📁 Location: dist/VisionAI.exe")
            if os.path.exists("dist/VisionAI.exe"):
                size_mb = os.path.getsize("dist/VisionAI.exe") / (1024*1024)
                print(f"📋 File size: {size_mb:.1f} MB")
            return True
        else:
            print(f"❌ PyInstaller error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running PyInstaller: {e}")
        return False

def create_installer_script():
    """Create a simple installer batch script"""
    installer_content = '''@echo off
echo ========================================
echo    VisionAI - Smart Camera Detection
echo ========================================
echo.

echo 📦 Installing VisionAI...

REM Create installation directory
if not exist "C:\\VisionAI" mkdir "C:\\VisionAI"

REM Copy executable
if exist "VisionAI.exe" (
    copy "VisionAI.exe" "C:\\VisionAI\\VisionAI.exe"
) else (
    echo ❌ VisionAI.exe not found!
    pause
    exit /b 1
)

REM Create desktop shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%USERPROFILE%\\Desktop\\VisionAI.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "C:\\VisionAI\\VisionAI.exe" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "C:\\VisionAI" >> CreateShortcut.vbs
echo oLink.Description = "VisionAI Smart Camera Detection" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs
del CreateShortcut.vbs

REM Create start menu shortcut
if not exist "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\VisionAI" mkdir "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\VisionAI"
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateStartMenu.vbs
echo sLinkFile = "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\VisionAI\\VisionAI.lnk" >> CreateStartMenu.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateStartMenu.vbs
echo oLink.TargetPath = "C:\\VisionAI\\VisionAI.exe" >> CreateStartMenu.vbs
echo oLink.WorkingDirectory = "C:\\VisionAI" >> CreateStartMenu.vbs
echo oLink.Description = "VisionAI Smart Camera Detection" >> CreateStartMenu.vbs
echo oLink.Save >> CreateStartMenu.vbs
cscript CreateStartMenu.vbs
del CreateStartMenu.vbs

echo.
echo ✅ VisionAI installed successfully!
echo 📍 Location: C:\\VisionAI\\VisionAI.exe
echo 🖥️ Desktop shortcut created
echo 📋 Start menu shortcut created
echo.
echo Press any key to exit...
pause >nul
'''
    
    with open("dist/Install_VisionAI.bat", "w") as f:
        f.write(installer_content)
    
    print("✅ Installer script created: dist/Install_VisionAI.bat")

def main():
    print("🚀 VisionAI Executable Builder")
    print("=" * 40)
    
    # Check if required files exist
    if not os.path.exists("vision_ai.py"):
        print("❌ vision_ai.py not found!")
        return
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Create executable
    if create_exe():
        create_installer_script()
        print("\n🎉 Build completed successfully!")
        print("\n📦 Distribution files:")
        print("   • dist/VisionAI.exe (Main executable)")
        print("   • dist/Install_VisionAI.bat (Installer script)")
        print("\n📋 To distribute:")
        print("   1. Copy both files to target PC")
        print("   2. Run Install_VisionAI.bat as Administrator")
        print("   3. VisionAI will be installed and shortcuts created")
        print("\n⚠️ Note: First run may be slow as it extracts files")
    else:
        print("❌ Build failed! Try the portable version instead:")
        print("   python create_portable.py")

if __name__ == "__main__":
    main()