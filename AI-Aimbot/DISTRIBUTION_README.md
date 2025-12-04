# AI Aimbot - Distribution Package

## For End Users

### Quick Start
1. Run `setup.bat` (one-time setup)
2. Double-click `AI_Aimbot_Launcher.exe` to start

### What Gets Installed
- Python virtual environment
- PyTorch with CUDA support
- Required dependencies (OpenCV, NumPy, etc.)

### System Requirements
- Windows 10/11
- 8GB RAM minimum
- NVIDIA GPU recommended (AMD/CPU also supported)
- 2GB free disk space

## For Developers

### Development Setup
1. Run `setup.bat` to create environment
2. Run `start_gui.bat` to launch GUI during development
3. Run `python main.py` for console-only mode

### Building for Distribution
1. Ensure virtual environment is set up: `setup.bat`
2. Run `build.bat` to create standalone executable
3. Distribute the contents of the `dist` folder along with:
   - `setup.bat`
   - `config.py` (template)
   - `main.py`
   - `gameSelection.py`
   - `utils/` folder
   - `models/` folder
   - `.onnx`/`.pt` model files

### Files Overview
- `start_gui.bat` - Launch GUI (development)
- `run.bat` - Launch console mode
- `setup.bat` - One-time environment setup
- `build.bat` - Build standalone executable
- `gui.py` - Modern GUI interface
- `main.py` - Core aimbot logic
- `config.py` - Configuration settings
- `gameSelection.py` - Window selection utility

### GUI Features
- Visual configuration interface
- Real-time settings adjustment
- Start/Stop controls
- Settings persistence
- Status monitoring

### Distribution Notes
When distributing, users will need:
1. The executable (`AI_Aimbot_Launcher.exe`)
2. `setup.bat` for initial environment setup
3. All Python files and model files
4. Instructions to run `setup.bat` first

The launcher will automatically use the virtual environment created by `setup.bat`.
