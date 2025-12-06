# AI Aimbot Launcher Build Script
# This creates a standalone executable for easy distribution

import PyInstaller.__main__
import os
import shutil
from pathlib import Path

# Clean previous builds
if os.path.exists('build'):
    shutil.rmtree('build')
if os.path.exists('dist'):
    shutil.rmtree('dist')

print("Building AI Aimbot Launcher...")

# PyInstaller arguments
PyInstaller.__main__.run([
    'gui.py',
    '--name=AI_Aimbot_Launcher',
    '--onefile',
    '--windowed',
    '--icon=NONE',  # Add icon path here if you have one
    '--add-data=config.py;.',
    '--add-data=main.py;.',
    '--add-data=gameSelection.py;.',
    '--add-data=requirements.txt;.',
    '--hidden-import=torch',
    '--hidden-import=cv2',
    '--hidden-import=numpy',
    '--hidden-import=bettercam',
    '--hidden-import=pygetwindow',
    '--hidden-import=pyautogui',
    '--collect-all=torch',
    '--collect-all=torchvision',
    '--noconfirm'
])

print("\n" + "="*50)
print("Build complete!")
print("Executable location: dist/AI_Aimbot_Launcher.exe")
print("="*50)
